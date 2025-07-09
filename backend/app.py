from flask import Flask, request, jsonify, send_from_directory
from db import collection
from utils import format_message
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')

@app.route("/webhook", methods=["POST"])
def webhook():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.get_json()
    data = format_message(event_type, payload)
    if data:
        collection.insert_one(data)
        return jsonify({"status": "success"}), 201
    return jsonify({"status": "ignored"}), 400

@app.route("/events", methods=["GET"])
def get_events():
    latest = list(collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(10))
    return jsonify(latest)

@app.route("/ui")
def serve_ui():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
