FROM python:3.11

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y locales
RUN apt-get install -y ffmpeg
RUN apt-get install -y build-essential
RUN pip3 install --upgrade pip

RUN locale-gen en_US.UTF-8
RUN chmod 0755 /etc/default/locale

ENV PYTHONIOENCODING=utf-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8
ENV RABBITMQ_USER=rabbitqm
ENV RABBITMQ_PASSWORD=rabbitqm

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "celery", "-A", "proj", "worker", "--loglevel=info", "--concurrency=50", "-Q", "io_bound", "--pool=gevent", "-n", "io_bound_worker@%h" ]
