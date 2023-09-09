from ydl import socketio
from ydl import app

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5888, debug=True)
