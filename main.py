from lxml import etree
from lxml.cssselect import CSSSelector
import cloudscraper

import time

#GLOBAL
SCRAPER = cloudscraper.create_scraper()
PARSER = etree.HTMLParser()
TOTAL_DEVIATION = 0.0
MOVIE_COUNT = 0
TOTAL_RATING_REQUEST_WAIT_TIME = 0

def ConstructDataLink(element):
    return "https://letterboxd.com" + element.get("data-item-link")

##
#takes a rated movie webpage and the rating of movies on the page
#todo needs verification it's not a timeout page
#
def DissectMovies(movieList, rating):
    movieGrid = movieList.cssselect('ul.-p70 li .react-component')
    for movie in movieGrid:
        global TOTAL_RATING_REQUEST_WAIT_TIME
        requestStartTime = time.perf_counter()
        avgRating = etree.fromstring(SCRAPER.get(ConstructDataLink(movie)).text[:3456], PARSER).cssselect('meta[name="twitter:data2"]')
        TOTAL_RATING_REQUEST_WAIT_TIME += (time.perf_counter() - requestStartTime)

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
    programStartTime = time.perf_counter()

    ratings = [.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]

    for rating in ratings:
        ratingStartTime = time.perf_counter()
        text = SCRAPER.get("https://letterboxd.com/jomimo/films/rated/" + str(rating) + "/by/rating/").text
        html_root  = etree.fromstring(text, PARSER)
        DissectMovies(html_root, rating)
        print("runtime for rating " + str(rating) + " is " + str(time.perf_counter() - ratingStartTime))

    print(TOTAL_DEVIATION / MOVIE_COUNT)
    print("movie count: " + str(MOVIE_COUNT))
    print("program runtime:" + str(time.perf_counter() - programStartTime))
    print("average request wait time for rating pages: " + str(TOTAL_RATING_REQUEST_WAIT_TIME / MOVIE_COUNT))





