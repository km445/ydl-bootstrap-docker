import os

from flask import Blueprint
from flask import request
from flask import Response
from flask import abort
from flask import session
from celery.result import AsyncResult

import config
from utils import get_and_rm_file
from controllers.downloader.downloader import YoutubeDLController
from proj.celery import app


downloader = Blueprint("downloader", __name__)


@downloader.route("/", methods=["GET", "POST"])
def youtube_dl():
    return YoutubeDLController(request).call()


@downloader.route("/results/<task_id>", methods=["GET", "POST"])
def get_result(task_id):
    result = AsyncResult(task_id, backend=app.backend)
    data = result.get(timeout=1)
    path = os.path.join(config.downloads_dir, session["sid"],
                        data.get("filename"))
    if not os.path.exists(path):
        abort(500)

    return Response(get_and_rm_file(path, result),
                    mimetype=data.get("mimetype"),
                    headers=data.get("headers"))
