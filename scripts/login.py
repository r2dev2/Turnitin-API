import requests
from bs4 import BeautifulSoup

import personal

LOGIN_URL = "https://www.turnitin.com/login_page.asp?lang=en_us"
HOMEPAGE = "https://www.turnitin.com/s_class_portfolio.asp"
headers={
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "sec-ch-ua": "\"Chromium\";v=\"85\", \"\\\\Not;A\\\"Brand\";v=\"99\", \"Microsoft Edge\";v=\"85\"",
    "content-type": "application/x-www-form-urlencoded",
    "referer": LOGIN_URL,
    "referrer": LOGIN_URL,
    "referrerPolicy": "no-referrer-when-downgrade",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
}
payload = f"javascript_enabled=0&email={personal.email}&user_password={personal.password}&submit=Log+in"

with requests.Session() as s:
    s.headers.update(headers)
    s.get(LOGIN_URL)
    cookies = s.cookies.get_dict()
    r = s.post(
        LOGIN_URL,
        data=payload.encode("utf-8")
    )
    source = r.content.decode("utf-8")
    with open("yet.html", "w+", encoding="utf-8") as fout:
        fout.write(source)
    soup = BeautifulSoup(source, "html.parser")
    classes = soup.find_all("td", {"class": "class_name"})
    for i in range(len(classes)):
        e = classes[i].find("a")
        classes[i] = {"title": e["title"], "url": f"https://www.turnitin.com/{e['href']}"}
        print(classes[i])

    print(classes[0]["url"])
    r = s.get(classes[0]["url"])
    with open("yet.html", 'w+') as fout:
        fout.write(r.content.decode("utf-8"))


