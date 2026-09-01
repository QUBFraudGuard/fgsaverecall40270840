import os
from flask import Flask, jsonify, request
from google.cloud import storage
import uuid, json

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response



client = storage.Client()
bucket = client.bucket("fgsaverecall-40270840")


@app.route("/save", methods=["POST", "OPTIONS"])
def save():
    if request.method == "OPTIONS":
        return "", 204
    batch_text = request.json.get("items", "")
    batch_id = str(uuid.uuid4())[:8]
    blob = bucket.blob(f"{batch_id}.json")
    blob.upload_from_string(json.dumps({"items": batch_text}), content_type="application/json")
    return jsonify({"id": batch_id})
    

@app.route("/recall/<batch_id>", methods=["GET"])
def recall(batch_id):
    blob = bucket.blob(f"{batch_id}.json")
    if not blob.exists():
        return jsonify({"error": "not found"}), 404
    return jsonify(json.loads(blob.download_as_text()))

    # A simple "are you alive?" endpoint. Handy for testing and for Docker.
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))