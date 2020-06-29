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
| `/submit` | `POST` | `{ auth: "auth", assignment: "assignment", title: "title", filename: "filename", firstname: "firstname", lastname: "lastname" }` | `{ char_count: uint, file_name: "file_name", file_size: "file_size", "image_url_stub": "path_to_image", page_count: uint, status: bool, uuid: "uuid", word_count: uint }`

## Examples
JavaScript:
```javascript
var email = "email@example.com";
var password = "password";
var host = "https://turnitin-api.herokuapp.com";
var authKeys;
var toDownload;
var pdf = false;
fetch(host + "/login", {
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    "body": JSON.stringify({email: email, password: password}),
    "method": "POST"
}).then(response=>{
    return response.json();
}).then(json=>{
    authKeys = json.auth;
}).then(()=>{
    return fetch(host + "/classes", {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        "body": JSON.stringify({auth: authKeys}),
        "method": "POST"
    });
}).then(response=>{
    return response.json();
}).then(classes=>{
    console.log(classes);
    return classes[0];
}).then(firstClass=>{
    return fetch(host + "/assignments", {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        "body": JSON.stringify({auth: authKeys, url: firstClass.url}),
        "method": "POST"
    });
}).then(response=>{
    return response.json();
}).then(assignments=>{
    console.log(assignments);
    return assignments[0];
}).then(assignment=>{
    toDownload = assignment;
    return fetch(host + "/download", {
        headers: {
            'Content-Type': 'application/json'
        },
        "body": JSON.stringify({auth: authKeys, assignment: toDownload, pdf: pdf}),
        "method": "POST"
    });
}).then(response=>{
    return response.blob();
}).then(blob=>{
    console.log(blob);
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    var filename = pdf?(toDownload.title+".pdf"):toDownload.file;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
});
```
```javascript
var email = "username";
var password = "password";
var host = "http://localhost:5000";
var authKeys;
fetch(host + "/login", {
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    "body": JSON.stringify({email: email, password: password}),
    "method": "POST"
}).then(response=>{
    return response.json();
}).then(json=>{
    authKeys = json.auth;
}).then(()=>{
    return fetch(host + "/classes", {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        "body": JSON.stringify({auth: authKeys}),
        "method": "POST"
    });
}).then(response=>{
    return response.json();
}).then(classes=>{
    console.log(classes);
    return classes[0];
}).then(firstClass=>{
    return fetch(host + "/assignments", {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        "body": JSON.stringify({auth: authKeys, url: firstClass.url}),
        "method": "POST"
    });
}).then(response=>{
    return response.json();
}).then(assignments=>{
    console.log(assignments);
    console.log(assignments[25]);
    return assignments[25];
}).then(assignment=>{
    var reader = new FileReader();
    var fileByteArray = [];
    reader.readAsArrayBuffer(document.querySelector('input').files[0]);
    reader.onloadend = function (evt) {
        if (evt.target.readyState == FileReader.DONE) {
           var arrayBuffer = evt.target.result,
               array = new Uint8Array(arrayBuffer);
           for (var i = 0; i < array.length; i++) {
               fileByteArray.push(array[i]);
            }
            toUpload = assignment;
            return fetch(host + "/submit", {
                headers: {
                    'Content-Type': 'application/json'
                },
                "body": JSON.stringify({
                    auth: authKeys,
                    assignment: toUpload,
                    submission:{
                        title: "test title",
                        filename: "test.docx",
                        file: fileByteArray
                    },
                    firstname: "Kento",
                    lastname: "Nishi"
                }
                ),
                "method": "POST"
            }).then(response=>{
                return response.json();
            }).then(json=>{
                console.log(json);
            });
        }
    }
});
```
Python 3:
```python
import requests

url = "https://turnitin-api.herokuapp.com"

USERNAME = "email@example.com"
PASSWORD = "password"


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
```
