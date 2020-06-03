import requests
from bs4 import BeautifulSoup

import personal

LOGIN_URL = "https://api.turnitin.com/login_page.asp?lang=en_us"
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
payload = personal.payload

with requests.Session() as s:
    s.headers.update(headers)
    s.get(LOGIN_URL)
    cookies = s.cookies.get_dict()
    r = s.post(
        LOGIN_URL,
        data=payload.encode("utf-8")
    )
    source = r.content.decode("utf-8")
    with open("yet.html", 'w+') as fout:
        fout.write(source)
    soup = BeautifulSoup(source, "html.parser")
    classes = soup.find_all("td", {"class": "class_name"})
    for e in (c.find('a') for c in classes):
        print(f"{e['title']}\nhttps://turnitin.com/{e['href']}\n")
    r = s.get(HOMEPAGE)
    with open("yet.html", 'w+') as fout:
        fout.write(r.content.decode("utf-8"))

