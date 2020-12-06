from flask import Flask, jsonify
from flask_socketio import SocketIO, emit, send
from eventlet import monkey_patch


monkey_patch()

app = Flask(__name__)
app.config["SECRET_KEY"] = "satoshi"
app.debug = True
app.host = "localhost"

socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on("run")
def run():
    from simulations.black_thursday import run_sim
    run_sim(socketio)

if __name__ == "__main__":
    socketio.run(app)
