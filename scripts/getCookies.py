import requests

import personal

LOGIN_URL = "https://www.turnitin.com/login_page.asp?lang=en_us"
payload = personal.payload

with requests.Session() as s:
    s.get(LOGIN_URL)
    cookies = s.cookies.get_dict()
    cookies["XSRF-TOKEN"] = "eyJpdiI6InhkaUVURWZ5RXRjM0d1NVArSTg5RWc9PSIsInZhbHVlIjoiazE5S1BOait3UFV4bGpHbFwvUmtXVmd3V0h0SlVHMVhleis4dm5qeEhsN0JQeWZ5QlBONFkzODQ2SWlXZE1vcG1WM1ozVlJnVUtteEwrU3Z3bU9ySlBRPT0iLCJtYWMiOiJhZjRiYjg4MmNjMGEzN2U4ZDllODQ1ZWU4YzM2OTU5YmE1YjllNWRlOGFiMDY4YmEyZTI5MGU1ZjJhOTI3ZmI5In0="
    cookies["laravel_session"] = cookies["XSRF-TOKEN"]
    print(cookies)
    # s.post(LOGIN_URL, data=payload.encode("utf-8"), cookies=cookies)
    r = s.post(
        LOGIN_URL,
        headers={
            "referer": LOGIN_URL,
        },
        data=payload.encode("utf-8")
    )
    # r = s.get("https://www.turnitin.com/s_home.asp", cookies=cookies)
    with open("yet.html", 'w+') as fout:
        fout.write(r.content.decode("utf-8"))
