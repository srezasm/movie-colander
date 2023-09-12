import requests
from urllib.parse import urlparse, urljoin
import re

__MOVIE_EXTENSIONS = ["mkv", "mp4"]


def __get_html(url):
    response = requests.get(url)
    return response.text


def __get_hrefs(html):
    regex = re.compile(
        r" href=\".*\"",
        re.IGNORECASE,
    )
    all_urls = regex.findall(html)

    return all_urls


def __get_extended_url(href, origin):
    origin_url = urlparse(origin)
    domain = origin_url.scheme + "://" + origin_url.netloc
    if not re.search(r"^https?\\", href):
        return urljoin(domain, href)
    return href


def extract_movie_urls(web_page_url: str) -> list:
    html = __get_html(web_page_url)
    hrefs = __get_hrefs(html)

    urls = []
    for href in hrefs:
        href = href.split('"')[1]
        if href.split(".")[-1] in __MOVIE_EXTENSIONS:
            urls.append(__get_extended_url(href, web_page_url))

    return urls
