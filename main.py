import requests
from lxml import etree
from lxml.cssselect import CSSSelector


def dissectMovie(j):
    print(f'Hi,')

def handlePagination():
    return

if __name__ == '__main__':
    parser = etree.HTMLParser()
    text = requests.get('https://letterboxd.com/jomimo/films/rated/5/by/date/', headers={"User-Agent": "Mozilla/5.0"}).text
    html_root  = etree.fromstring(text, parser)
    print(text)
    var = html_root.cssselect('ul.grid')
    print(1)
