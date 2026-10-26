"""The Flask server. Run it with:  python app.py"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from seed import DEMO_MACHINES, PARAMETERS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")


@app.get("/api/health")
def health():
    return jsonify({"ok": True})


@app.get("/api/machines")
def machines():
    return jsonify([{**m, "parameters": PARAMETERS[m["type"]]} for m in DEMO_MACHINES])


if __name__ == "__main__":
    # FR-28e: for https, give the server a certificate (see SETUP.md, "Secure connection").
    socketio.run(app, host="127.0.0.1", port=5000, allow_unsafe_werkzeug=True)
