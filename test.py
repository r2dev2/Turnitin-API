import requests
import json

url = "https://turnitin-api.herokuapp.com"
USERNAME = "email@example.com"
PASSWORD = "password"

with requests.Session() as s:
    login_result = s.post(url + "/login", json={
        "email": USERNAME,
        "password": PASSWORD
    })
    auth = json.loads(login_result.text)
    print(auth)

    classes_result = s.post(url + "/classes", json=auth)
    classes = json.loads(classes_result.text)
    print(classes[0])

    first_class_data = dict(auth)
    first_class_data["url"] = classes[0]["url"]
    assignments_result = s.post(url + "/assignments", json=first_class_data)
    assignments = json.loads(assignments_result.text)
    print(assignments[0])

