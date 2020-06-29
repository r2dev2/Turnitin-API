# Turnitin-API
An unofficial REST API for Turnitin.

## Endpoints

All endpoints are relative to [https://turnitin-api.herokuapp.com](https://turnitin-api.herokuapp.com).

| URL | Method | Data | Response |
|:----|:-------|:-----|:---------|
| `/login` | `POST` | `{ email: "email", password: "password" }` | `{ auth: [json] }` |
| `/classes` | `POST` | `{ auth: [json] } ` | `[{title: "title", url: "url"}, ...]` |
| `/assignments` | `POST` | `{ auth: [json], url: "url" }` | `[{ title: "title", dates: { due: "due", post: "post", start: "start" }, info: "info", submission: "url" }, ...]` |
| `/download` | `POST` | `{ auth: [json], assignment: [json], pdf: [true/false] } ` | Raw bytes of file submitted |

| URL | Method | Form | Response |
|:----|:-------|:-----|:---------|
| `/submit` | `POST` | `{ auth: "auth", assignment: "assignment", title: "title", filename: "filename" }` | `{ char_count: uint, file_name: "file_name", file_size: "file_size", "image_url_stub": "path_to_image", page_count: uint, status: bool, uuid: "uuid", word_count: uint }`

# Examples

Python 3:
```python
import json
import requests

url = "https://turnitin-api.herokuapp.com"

USERNAME = "email@example.com"
PASSWORD = "password"

FIRSTNAME = "Michael"
LASTNAME = "Reeves"


with requests.Session() as s:
    login_result = s.post(url + "/login", json={
        "email": USERNAME,
        "password": PASSWORD
    })
    auth = login_result.json()

    classes_result = s.post(url + "/classes", json=auth)
    classes = classes_result.json()
    for c in classes:
        if "World Lit" in c["title"]:
            world_lit = c
    print(world_lit)

    first_class_data = dict(auth, url=world_lit["url"])
    assignments_result = s.post(url + "/assignments", json=first_class_data)
    assignments = assignments_result.json()
    print(assignments[0])

    download_query = dict(**auth, assignment=assignments[0], pdf=True)
    r = s.post(url + '/download', json=download_query)
    print(f"Status code {r.status_code}")
    with open("test_download.pdf", 'wb+') as fout:
        fout.write(r.content)

    # In this example case, the fourth assignment 
    uf = open("Document.docx", 'rb')
    submit_query = dict(auth=json.dumps(auth["auth"]), assignment=json.dumps(assignments[3]),
                        title="test submission 1", filename="Document.docx")
    r = s.post(url + "/submit", data=submit_query, files={"userfile": uf})
    print(r.json())
```
