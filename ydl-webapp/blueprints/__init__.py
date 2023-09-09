from ydl import app
from .downloader import downloader
from .error import errors

app.register_blueprint(downloader)
app.register_blueprint(errors)
