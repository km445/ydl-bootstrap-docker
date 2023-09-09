result_backend = 'redis://redis:6379/0'
result_expires = 60 * 15
broker_url = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
task_serializer = 'json'
result_serializer = 'json'
include = ['proj.tasks']
task_routes = {"proj.tasks.download_file_cpu_bound": "cpu_bound",
               "proj.tasks.download_file_io_bound": "io_bound"}
