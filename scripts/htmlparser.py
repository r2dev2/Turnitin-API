from bs4 import BeautifulSoup

def get_assignment_title(e):
    return e.find("td", {"class": "title"}).find("div").text

def get_info(e):
    return e.find("td", {"class": "info"}).find("button").find("div").text

def get_dates(e):
    raw_dates = e.find_all("td")[2].find("div").find_all("div", {"class": "tooltip"})
    return {
        "Start": {
            "Date": raw_dates[0].find("div", {"class": "date start-date"}).text,
            "Time": raw_dates[0].find("div", {"class": "time start-time"}).text
        },
        "Due": {
            "Date": raw_dates[1].find("div", {"class": "date due-date"}).text,
            "Time": raw_dates[1].find("div", {"class": "time due-time"}).text
        },
        "Post": {
            "Date": raw_dates[2].find("div", {"class": "date post-date"}).text,
            "Time": raw_dates[2].find("div", {"class": "time post-time"}).text
        }
    }

def get_submission_link(e):
    return e.find("td", {"class": "action-buttons"}).find("a")["href"]

def get_assignment_table(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all("tr", {"class": "Paper"})

