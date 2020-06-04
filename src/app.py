from flask import Flask, request, jsonify
import json
import os
import turnitin

app = Flask(__name__, static_url_path="")
algo = None


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


if __name__ == "__main__":
    app.run()

"""
Client side js, run in the browser:
fetch("login", {
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    "body": JSON.stringify({email:email, password: password}),
    "method": "POST"
}).then(response=>{
    response.json().then(json=>{
        console.log(json);
    });
});
"""
