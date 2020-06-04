# Turnitin-API
An unofficial REST API for Turnitin.

## Endpoints

All endpoints are relative to [https://turnitin-api.herokuapp.com](https://turnitin-api.herokuapp.com).

| URL | Method | Data | Response |
|:----|:-------|:-----|:---------|
| `/login` | `POST` | `{ email: "email", password: "password" }` | `{ auth: [json] }` |
| `/classes` | `POST` | `{ auth: [json]} ` | `[{title: "title", url: "url"}, ...]` |
| `/assignments` | `POST` | `{ auth: [json], url: "url" }` | `{ title: "title", dates: { due: "due", post: "post", start: "start" }, info: "info", submission: "url" }` |

## Examples
JavaScript:
```javascript
var email = "email@example.com"
var password = "password";
var authKeys;
fetch("https://turnitin-api.herokuapp.com/login", {
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
    return fetch("https://turnitin-api.herokuapp.com/classes", {
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
    return fetch("https://turnitin-api.herokuapp.com/assignments", {
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
});
```