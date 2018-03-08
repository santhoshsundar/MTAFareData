import re
from bs4 import BeautifulSoup
from requests import get
from datetime import datetime

MTA_FARE_URL = "http://web.mta.info/developers/fare.html"
MTA_ROOT_URL = "http://web.mta.info/developers/"

"""
Get links from MTA Fare Data
"""


def get_site():
    url = get(MTA_FARE_URL)
    return url


def get_fare_links(response):

    soup = BeautifulSoup(response.content, 'lxml')
    links = soup.find('div', class_='span-19 last')
    links_href = links.find_all('a')
    fare_links = [(link.text, MTA_ROOT_URL + link['href']) for link in links_href]
    return fare_links


def get_links():
    return get_fare_links(get_site())


def get_fare_date(start, end):
    links = get_links()
    in_range = []
    for text, link in links:
        date = datetime.strptime(text, "%A, %B %d, %Y")
        if date >= start and date <= end:
            in_range.append(link)

    return in_range
