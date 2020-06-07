import json
import os
import sys

from flask import Flask, jsonify, redirect, request, send_file
from flask_cors import CORS

import turnitin

app = Flask(__name__, static_url_path="")
CORS(app)


@app.before_request
def before_request():
    if not app.debug and request.url.startswith("http://"):
        url = request.url.replace("http://", "https://", 1)
        code = 301
        return redirect(url, code=code)


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    return jsonify({"auth": turnitin.login(data["email"], data["password"])})


@app.route("/classes", methods=["POST"])
def getClasses():
    data = request.get_json()
    return jsonify(turnitin.getClasses(data["auth"]))


@app.route("/assignments", methods=["POST"])
def getAssignments():
    data = request.get_json()
    return jsonify(turnitin.getAssignments(data["url"], data["auth"]))


@app.route("/download", methods=["POST"])
def getDownload():
    data = request.get_json()
    fileBytes = turnitin.getDownload(
        data["auth"],
        data["assignment"]["oid"],
        data["assignment"]["title"],
        data["pdf"],
    )
    return fileBytes


@app.route("/")
def index():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run(debug=(not "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")))
