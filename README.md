# JYDL flask/celery/socketio/jquery/bootstrap + docker
JYDL - Jquery Youtube Downloader application with docker
(because everybody and his brother seem to want docker these days, without caring to realize pitfalls and dangers whatsoever)

## Application demo instructions

Note: you take it upon yourself to install docker and docker-compose, which are installed separately; use these links as a guide:
1. https://docs.docker.com/v17.09/engine/installation/linux/docker-ce/ubuntu/#install-docker-ce
1. https://docs.docker.com/compose/install/

1. Clone the project `git clone https://github.com/km445/ydl-bootstrap-docker.git`.
1. Run `docker-compose up --build`.
1. Go to `localhost:5888` in your browser to use the application.

Some more notes:
1. Before running docker-compose make sure that ports 5672, 15672, 5888, 6379 are not occupied, otherwise docker-compose probably won't start.
