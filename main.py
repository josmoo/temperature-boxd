from lxml import etree
from lxml.cssselect import CSSSelector
import cloudscraper

def dissectMovie(j):
    print(f'Hi,')

def handlePagination():
    return

def constructDataLink(element):
    return "https://letterboxd.com" + element.get("data-item-link")

if __name__ == '__main__':

    scraper = cloudscraper.create_scraper()
    parser = etree.HTMLParser()
    text = scraper.get("https://letterboxd.com/jomimo/films/rated/5/by/date/").text
    html_root  = etree.fromstring(text, parser)
    var = html_root.cssselect('ul.-p70 li .react-component')
    var2 = list(map(constructDataLink, var))
    print(1)
