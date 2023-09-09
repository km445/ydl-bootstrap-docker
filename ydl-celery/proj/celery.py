import os

from celery import Celery

from config import celery_logs

app = Celery('proj')
app.config_from_object('proj.celeryconfig')

if not os.path.exists(celery_logs):
    os.mkdir(celery_logs)

if __name__ == "__main__":
    app.start()
