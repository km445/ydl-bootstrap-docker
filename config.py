import logging
from datetime import datetime

logs_dir = "logs"
celery_logs = "proj/logs"
downloads_dir = "downloads"
log_config = {"level": logging.DEBUG,
              "filename": ("%s/logs_%s.log" %
                           (logs_dir, datetime.now().strftime("%Y-%m-%d"))),
              "format": (logging
                         .Formatter("%(asctime)s [%(thread)d:%(threadName)s] "
                                    "[%(levelname)s] - %(name)s: %(message)s"))
              }

# flask app secret key
secret_key = 'some_secret'

# Maximum download size in bytes
max_filesize = 1024 * 1024 * 1024 * 10

# socketio queue; should be the same as rabbitmq vhost
message_queue = "amqp://rabbitmq:rabbitmq@rabbit:5672/socketio"

# socketio namespace; namespace used for socketio tasks
namespace = "/socketio_tasks"
