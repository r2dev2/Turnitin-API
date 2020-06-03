import requests
from bs4 import BeautifulSoup

__LOGIN_URL = "https://www.turnitin.com/login_page.asp?lang=en_us"
__HOMEPAGE = "https://www.turnitin.com/s_class_portfolio.asp"
__HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "sec-ch-ua": '"Chromium";v="85", "\\\\Not;A\\"Brand";v="99", "Microsoft Edge";v="85"',
    "content-type": "application/x-www-form-urlencoded",
    "referer": __LOGIN_URL,
    "referrer": __LOGIN_URL,
    "referrerPolicy": "no-referrer-when-downgrade",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
}
__session = None


def login(email, password):
    global __session
    payload = f"javascript_enabled=0&email={email}&user_password={password}&submit=Log+in".encode(
        "utf-8"
    )
    __session = requests.Session()
    cookies = __getCookies(__LOGIN_URL)
    __setCookies(cookies)
    with open("dashboard.html", "w+", encoding="utf-8") as fout:
        fout.write(__post(__LOGIN_URL, payload))


def __resetHeaders():
    __session.headers.update(__HEADERS)


def __post(url, payload):
    __resetHeaders()
    return __session.post(url, data=payload).content.decode("utf-8")


def __get(url):
    __resetHeaders()
    return __session.get(url).content.decode("utf-8")


def __getCookies(url):
    __session.get(url)
    cookies = __session.cookies
    return cookies


def __setCookies(cookies):
    __session.cookies.update(cookies)

