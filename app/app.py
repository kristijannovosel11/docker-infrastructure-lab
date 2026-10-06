import os

from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify(
        service="docker-infrastructure-lab",
        version=os.getenv("APP_VERSION", "1.0.0"),
        hostname=os.getenv("HOSTNAME", "unknown"),
    )


@app.get("/health")
def health():
    return jsonify(status="ok"), 200
