import os
import logging

import config


class Log(object):
    """File logger class"""

    def __init__(self, file_handler, log_name):
        self._log = logging.getLogger(log_name)
        self._log.addHandler(file_handler)
        self._log.setLevel(file_handler.level)

    def __getattr__(self, *args, **kwargs):
        return getattr(self._log, *args, **kwargs)


def get_and_rm_file(path, result):
    if not os.path.exists(path):
        raise StopIteration()
    with open(path, "rb") as f:
        yield from f

    os.remove(path)
    result.forget()


def send_message(s, event, room, message):
    s.emit(event, message, namespace=config.namespace, room=room)


def get_request_data(request):
    return dict(request.form.items() or request.json or {})
