import requests
from bs4 import BeautifulSoup

import personal
from parser import *

LOGIN_URL = "https://www.turnitin.com/login_page.asp?lang=en_us"
HOMEPAGE = "https://www.turnitin.com/s_class_portfolio.asp"
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "sec-ch-ua": '"Chromium";v="85", "\\\\Not;A\\"Brand";v="99", "Microsoft Edge";v="85"',
    "content-type": "application/x-www-form-urlencoded",
    "referer": LOGIN_URL,
    "referrer": LOGIN_URL,
    "referrerPolicy": "no-referrer-when-downgrade",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
}
payload = f"javascript_enabled=0&email={personal.email}&user_password={personal.password}&submit=Log+in"


def post(s, url):
    r = s.post(url, data=payload.encode("utf-8"))
    source = r.content.decode("utf-8")
    return source


def get(s, url):
    r = s.get(url, data=payload.encode("utf-8"))
    source = r.content.decode("utf-8")
    return source


def setCookies(s, url):
    s.headers.update(headers)
    s.get(url)
    cookies = s.cookies.get_dict()


with requests.Session() as s:
    setCookies(s, LOGIN_URL)
    source = post(s, LOGIN_URL)
    with open("yet.html", "w+", encoding="utf-8") as fout:
        fout.write(source)
    soup = BeautifulSoup(source, "html.parser")
    classes = soup.find_all("td", {"class": "class_name"})
    for i in range(len(classes)):
        e = classes[i].find("a")
        classes[i] = {
            "title": e["title"],
            "url": f"https://www.turnitin.com/{e['href']}",
        }
        print("Class " + (str)(i + 1) + ": " + classes[i]["title"])
    index = int(input("Class to fetch: ")) - 1
    source = get(s, classes[index]["url"])
    with open("yet.html", "w+", encoding="utf-8") as fout:
        fout.write(source)
    
    table = get_assignment_table(source)
    print(get_assignment_title(table[3]))
    print(get_info(table[3]))
    print(get_dates(table[3]))
    print(get_submission_link(table[3]))

