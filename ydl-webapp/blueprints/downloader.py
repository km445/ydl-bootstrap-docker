import os

from flask import Blueprint
from flask import request
from flask import abort
from flask import session
from flask import send_file
from flask import after_this_request
from celery.result import AsyncResult

import config
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

    @after_this_request
    def rm_file(response):
        os.remove(path)
        result.forget()
        return response

    return send_file(path, mimetype=data.get("mimetype"), as_attachment=True)
