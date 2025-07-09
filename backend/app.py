from flask import Flask, request, jsonify, send_from_directory
from db import collection
from utils import format_message
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='../frontend', static_url_path='')

@app.route("/", methods=["GET"])
def index():
    return "Webhook Receiver Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.get_json()

    data = format_message(event_type, payload)
    if data:
        collection.insert_one(data)
        return jsonify({"status": "success", "data": data}), 201
    else:
        return jsonify({"status": "ignored", "reason": "unsupported event or action"}), 400

@app.route("/events", methods=["GET"])
def get_events():
    latest = list(collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(10))
    return jsonify(latest)

# Serve index.html
@app.route("/ui")
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")

# Serve JS and CSS
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, port=port)
