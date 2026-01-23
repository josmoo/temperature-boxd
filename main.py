from lxml import etree
from lxml.cssselect import CSSSelector
import cloudscraper

#GLOBAL
SCRAPER = cloudscraper.create_scraper()
PARSER = etree.HTMLParser()
TOTAL_DEVIATION = 0.0
MOVIE_COUNT = 0

def ConstructDataLink(element):
    return "https://letterboxd.com" + element.get("data-item-link")

##
#takes a rated movie webpage and the rating of movies on the page
# TODO: desperately needs to be optimized. obvious first optimization is to not parse the entire html for just a rating
def DissectMovies(movieList, rating):
    movieGrid = movieList.cssselect('ul.-p70 li .react-component')
    movieLinks = list(map(ConstructDataLink, movieGrid))
    for movieLink in movieLinks:
        avgRating = etree.fromstring(SCRAPER.get(movieLink).text, PARSER).cssselect('meta[name="twitter:data2"]')
        if avgRating:
            global TOTAL_DEVIATION
            global MOVIE_COUNT
            TOTAL_DEVIATION += abs(rating - float(avgRating[0].get('content')[:4]))
            MOVIE_COUNT += 1

        else:
            print("no one watches this shit movie sorry")


    return

def HandlePagination():
    return


if __name__ == '__main__':

    ratings = [.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]

    for rating in ratings:
        text = SCRAPER.get("https://letterboxd.com/jomimo/films/rated/" + str(rating) + "/by/rating/").text
        html_root  = etree.fromstring(text, PARSER)
        DissectMovies(html_root, rating)

print(TOTAL_DEVIATION / MOVIE_COUNT)

