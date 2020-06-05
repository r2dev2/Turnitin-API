from flask import Flask, request, jsonify, send_file
import json
import os
import turnitin
from flask_cors import CORS

app = Flask(__name__, static_url_path="")
CORS(app)


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


@app.route("/submission", methods=["POST"])
def getDownload():
    data = request.get_json()
    fileBytes = turnitin.getDownload(
        data["auth"], data["oid"], data["name"], data["pdf"]
    )
    return jsonify(fileBytes)


@app.route("/")
def index():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run()
