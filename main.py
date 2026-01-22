from lxml import etree
from lxml.cssselect import CSSSelector
import cloudscraper

def ConstructDataLink(element):
    return "https://letterboxd.com" + element.get("data-item-link")

def DissectMovies(movieList, rating):
    movieGrid = movieList.cssselect('ul.-p70 li .react-component')
    movieLinks = list(map(ConstructDataLink, movieGrid))
    for movieLink in movieLinks:
        avgRating = etree.fromstring(scraper.get(movieLink).text, parser).cssselect('meta[name="twitter:data2"]')
        if avgRating:
            print(avgRating[0].get('content'))
        else:
            print("no one watches this shit movie sorry")
    return

def HandlePagination():
    return

#GLOBAL
scraper = cloudscraper.create_scraper()
parser = etree.HTMLParser()

if __name__ == '__main__':

    ratings = [".5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]

    for rating in ratings:
        text = scraper.get("https://letterboxd.com/jomimo/films/rated/" + rating + "/by/rating/").text
        html_root  = etree.fromstring(text, parser)
        DissectMovies(html_root, rating)
        print(1)
