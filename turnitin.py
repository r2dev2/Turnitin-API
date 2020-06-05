import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re

__LOGIN_URL = "https://www.turnitin.com/login_page.asp?lang=en_us"
__HOMEPAGE = "https://www.turnitin.com/s_class_portfolio.asp"
__DOWNLOAD_URL = "https://www.turnitin.com/paper_download.asp"
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


def login(email, password):
    s = __newSession()
    payload = f"javascript_enabled=0&email={email}&user_password={password}&submit=Log+in".encode(
        "utf-8"
    )
    cookies = __getCookies(s, __LOGIN_URL)
    __setCookies(s, cookies)
    __post(s, __LOGIN_URL, payload)
    return cookies.get_dict()


def getClasses(cookies):
    s = __newSession()
    __setCookies(s, cookies)
    source = __get(s, __HOMEPAGE)
    classes = __parseDashboard(source)
    return classes


def getAssignments(url, cookies):
    s = __newSession()
    __setCookies(s, cookies)
    source = __get(s, url)
    table = __getAssignmentTable(source)
    return [
        {
            "title": __getAssignmentTitle(assignment),
            "info": __getAssignmentInfo(assignment),
            "dates": __getAssignmentDate(assignment),
            "submission": __getSubmissionLink(assignment),
            "oid": __getOid(assignment),
            "file": __getFileName(assignment),
        }
        for assignment in table
    ]


def getDownload(cookies, oid, filename, pdf):
    s = __newSession()
    __setCookies(s, cookies)
    query = {"oid": oid, "fn": filename, "type": "paper", "p": int(pdf)}
    return s.get(__DOWNLOAD_URL, params=query).content


def __newSession():
    return requests.Session()


def __parseDashboard(source):
    soup = BeautifulSoup(source, "html.parser")
    classes = soup.find_all("td", {"class": "class_name"})
    for i in range(len(classes)):
        e = classes[i].find("a")
        classes[i] = {
            "title": e["title"],
            "url": f"https://www.turnitin.com/{e['href']}",
        }
    return classes


def __resetHeaders(s):
    s.headers.update(__HEADERS)


def __post(s, url, payload):
    __resetHeaders(s)
    return s.post(url, data=payload).content.decode("utf-8")


def __get(s, url):
    __resetHeaders(s)
    return s.get(url).content.decode("utf-8")


def __getCookies(s, url):
    s.get(url)
    cookies = s.cookies
    return cookies


def __setCookies(s, cookies):
    s.cookies.update(cookies)


def __getAssignmentTitle(e):
    return e.find("td", {"class": "title"}).find("div").text


def __getAssignmentInfo(e):
    info = e.find("td", {"class": "info"}).find("button").find("div").text
    info = re.sub(r"\s\s+", " ", info)
    info = info.replace("\n", " ")
    info = info.replace(" Assignment Instructions ", "", 1)
    info = info[:-1]
    return info


def __convertDate(raw):
    date = raw.find("div", {"class": "date"}).text
    time = raw.find("div", {"class": "time"}).text
    dateObject = datetime.strptime(date + " " + time, "%d-%b-%Y %I:%M%p")
    return dateObject.strftime("%m/%d/%Y %H:%M:%S")


def __getAssignmentDate(e):
    raw_dates = e.find_all("td")[2].find("div").find_all("div", {"class": "tooltip"})
    return {
        "start": __convertDate(raw_dates[0]),
        "due": __convertDate(raw_dates[1]),
        "post": __convertDate(raw_dates[2]),
    }


def __getSubmissionLink(e):
    return e.find("td", {"class": "action-buttons"}).find("a")["href"]


def __getOid(e):
    try:
        return re.search("(/d+)", e.find("a")["id"]).group(1)
    except KeyError:
        return "void"


def __getFileName(e):
    try:
        return re.search("fn=(.+)\&type", e.find("a")["onclick"]).group(1)
    except KeyError:
        return "void"
    except AttributeError:
        return "void"


def __getAssignmentTable(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all("tr", {"class": "Paper"})
