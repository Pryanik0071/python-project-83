from datetime import date

from bs4 import BeautifulSoup
import requests


def parse_url(url):
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        return
    soup = BeautifulSoup(response.text, 'html.parser')
    return {
        'code': response.status_code,
        'h1': get_text(soup.find('h1')),
        'title': get_text(soup.find('title')),
        'desc': get_content(soup.find('meta', {'name': 'description'})),
        'date': date.today()
    }


def get_text(element):
    if element is None:
        return ''
    return element.text


def get_content(element):
    if element is None:
        return ''
    return element['content']
