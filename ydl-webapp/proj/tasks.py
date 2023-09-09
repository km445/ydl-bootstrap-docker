from celery.signals import after_task_publish
from flask_socketio import SocketIO
from celery.utils.log import get_task_logger

import config
from .celery import app as celery_app

socketio = SocketIO(message_queue=config.message_queue)
logger = get_task_logger(__name__)


@after_task_publish.connect
def update_sent_state(sender=None, headers=None, **kwargs):
    task = celery_app.tasks.get(sender)
    backend = task.backend if task else celery_app.backend
    backend.store_result(headers["id"], None, "SENT")


@celery_app.task(bind=True)
def download_file_io_bound(self, ydl_opts, default_ydl_opts, url, session_id,
                           cpu_bound_on_error=False, adjust_volume=False,
                           volume_factor=None):
    pass


@celery_app.task(bind=True)
def download_file_cpu_bound(self, ydl_opts, url, session_id):
    pass
