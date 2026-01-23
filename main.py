from lxml import etree
from lxml.cssselect import CSSSelector
import cloudscraper

import time

#GLOBAL
SCRAPER = cloudscraper.create_scraper()
PARSER = etree.HTMLParser()
TOTAL_DEVIATION = 0.0
MOVIE_COUNT = 0

def ConstructDataLink(element):
    return "https://letterboxd.com" + element.get("data-item-link")

##
#takes a rated movie webpage and the rating of movies on the page
#
def DissectMovies(movieList, rating):
    movieGrid = movieList.cssselect('ul.-p70 li .react-component')
    for movie in movieGrid:
        avgRating = etree.fromstring(SCRAPER.get(ConstructDataLink(movie)).text[:3456], PARSER).cssselect('meta[name="twitter:data2"]')
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
    start_time = time.perf_counter()

    ratings = [.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]

    for rating in ratings:
        text = SCRAPER.get("https://letterboxd.com/sarkovos/films/rated/" + str(rating) + "/by/rating/").text
        html_root  = etree.fromstring(text, PARSER)
        DissectMovies(html_root, rating)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print(TOTAL_DEVIATION / MOVIE_COUNT)

    print(f"Elapsed time: {elapsed_time:.4f} seconds")





