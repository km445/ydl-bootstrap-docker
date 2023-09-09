import os
import subprocess

from celery.signals import after_task_publish
from flask_socketio import SocketIO
from celery.utils.log import get_task_logger
import yt_dlp

import config
from .celery import app as celery_app
from constants import mimetypes
from constants import TaskStatuses
from constants import SocketEvents
from utils import send_message

socketio = SocketIO(message_queue=config.message_queue)
logger = get_task_logger(__name__)


class ETA(object):
    def __init__(self, task_id, session_id):
        self.session_id = session_id
        self.task_id = task_id

    def eta(self, d):
        if d.get("status") == "downloading":
            send_message(socketio, SocketEvents.TaskUpdate, self.session_id,
                         {"task_id": self.task_id,
                          "status": TaskStatuses.Downloading,
                          "extra": {"percent_completed": d.get("_percent_str"),
                                    "dl_speed": d.get("_speed_str"),
                                    "dl_size": d.get("_total_bytes_str")}})
        elif d.get("status") == "finished":
            send_message(socketio, SocketEvents.TaskUpdate, self.session_id,
                         {"task_id": self.task_id,
                          "status": TaskStatuses.Processing,
                          "extra": {"dl_finished": True}})


@after_task_publish.connect
def update_sent_state(sender=None, headers=None, **kwargs):
    task = celery_app.tasks.get(sender)
    backend = task.backend if task else celery_app.backend
    backend.store_result(headers["id"], None, "SENT")


@celery_app.task(bind=True)
def download_file_io_bound(self, ydl_opts, default_ydl_opts, url, session_id,
                           cpu_bound_on_error=False, adjust_volume=False,
                           volume_factor=None):
    logger.info("Processing task %s" % self.request.id)
    try:
        result = get_result(
            ydl_opts, url, self.request.id, session_id,
            adjust_volume=adjust_volume, volume_factor=volume_factor)
    except yt_dlp.utils.YoutubeDLError as e:
        logger.exception(e)
        result = get_result(
            default_ydl_opts, url, self.request.id, session_id,
            adjust_volume=adjust_volume, volume_factor=volume_factor)
    return result


@celery_app.task(bind=True)
def download_file_cpu_bound(self, ydl_opts, url, session_id):
    result = get_result(ydl_opts, url, self.request.id, session_id)
    return result


def get_result(ydl_opts, url, task_id, session_id,
               adjust_volume=False, volume_factor=None):
    ydl_opts["progress_hooks"] = [ETA(task_id, session_id).eta]
    send_message(socketio, SocketEvents.TaskUpdate, session_id,
                 {"task_id": task_id, "status": TaskStatuses.DownloadPending,
                  "extra": {}})
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        filename, info_dict = get_filename(ydl, url)
        send_message(socketio, SocketEvents.TaskUpdate, session_id,
                     {"task_id": task_id, "status": TaskStatuses.Processing,
                      "extra": {"title": info_dict.get("title"),
                                "thumbnail": info_dict.get("thumbnail")}})
        filesize = info_dict.get("filesize")
        if filesize and filesize > config.max_filesize:
            send_message(socketio, SocketEvents.TaskUpdate, session_id,
                         {"task_id": task_id, "status": TaskStatuses.Error,
                          "error":
                          "Maximum download size exceeded, \
                          please try a smaller download."})
            return {}
        ydl.extract_info(url, download=True)
        fn = get_fn_match(filename, session_id)
        if fn is None:
            send_message(socketio, SocketEvents.TaskUpdate, session_id,
                         {"task_id": task_id, "status": TaskStatuses.Error,
                          "error":
                          "Failed to fetch download, please try again."})
            return {}
        if adjust_volume and volume_factor is not None:
            get_adjusted_volume(session_id, fn, volume_factor)
        headers = {"Content-Disposition": 'attachment; filename="%s"' % fn}
        mimetype = get_mimetype(fn)
        if mimetype is None:
            send_message(socketio, SocketEvents.TaskUpdate, session_id,
                         {"task_id": task_id, "status": TaskStatuses.Error,
                          "error":
                          "Failed to fetch download, please try again."})
            return {}
        send_message(socketio, SocketEvents.TaskUpdate, session_id,
                     {"task_id": task_id, "status": TaskStatuses.Completed,
                      "extra": {}})
        return {"filename": fn, "mimetype": mimetype, "headers": headers}


def get_filename(ydl, url, with_extension=False):
    info_dict = ydl.extract_info(url, download=False)
    fn = ydl.prepare_filename(info_dict)
    if with_extension:
        return os.path.basename(fn), info_dict
    filename, ext = os.path.splitext(fn)
    return os.path.basename(filename), info_dict


def get_fn_match(filename, session_id):
    for fn in os.listdir(os.path.join(config.downloads_dir, session_id)):
        if filename in fn:
            return fn


def get_mimetype(fn):
    filename, ext = os.path.splitext(fn)
    return mimetypes.get(ext)


def get_adjusted_volume(session_id, fn, volume_factor):
    volume_factor = "%.1f" % volume_factor
    output_file_name = "Adjusted %s" % fn
    output_file_path = os.path.join(config.downloads_dir, session_id, output_file_name)
    input_file_path = os.path.join(config.downloads_dir, session_id, fn)
    call = " ".join(["ffmpeg", "-i", "'%s'" % input_file_path, "-af",
                     "volume=%s" % volume_factor, "'%s'" % output_file_path])
    process = subprocess.Popen(call, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result, err = process.communicate()
    os.rename(output_file_path, input_file_path)
