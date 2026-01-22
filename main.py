from lxml import etree
from lxml.cssselect import CSSSelector
import cloudscraper

def dissectMovie(j):
    print(f'Hi,')

def handlePagination():
    return

if __name__ == '__main__':

    scraper = cloudscraper.create_scraper()


    parser = etree.HTMLParser()
    text = scraper.get("https://letterboxd.com/jomimo/films/rated/5/by/date/").text
    html_root  = etree.fromstring(text, parser)
    print(text)
    var = html_root.cssselect('ul.grid')
    print(1)
