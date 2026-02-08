from lxml import etree
from lxml.cssselect import CSSSelector
import cloudscraper
import asyncio

import time
from pip import _internal
_internal.main(['list'])

#GLOBAL
SCRAPER = cloudscraper.create_scraper(
    interpreter='js2py',        # Best compatibility for v3 challenges

    # # Enhanced bypass features
    # enable_tls_fingerprinting=True,
    # enable_tls_rotation=True,
    # enable_anti_detection=True,
    # enable_enhanced_spoofing=True,
    # spoofing_consistency_level='medium',
    # enable_intelligent_challenges=True,
    # enable_adaptive_timing=True,
    # behavior_profile='focused',
    # enable_ml_optimization=True,
    # enable_enhanced_error_handling=True,

    # Stealth mode
    enable_stealth=True,
    stealth_options={
        'min_delay': .2,  # Minimum delay between requests
        'max_delay': 2.0,  # Maximum delay between requests
        'human_like_delays': True,  # Use human-like delay patterns
        'randomize_headers': True,  # Randomize request headers
        'browser_quirks': True,  # Enable browser-specific quirks
        'simulate_viewport': True,  # Simulate viewport changes
        'behavioral_patterns': True  # Use behavioral pattern simulation
    },

    # # Session management
    # session_refresh_interval=3600,
    # auto_refresh_on_403=True,
    # max_403_retries=3,

    browser='chrome'
)
SCRAPER._max_request_depth = 500 #big uh oh no no bandaid fix todo fix
PARSER = etree.HTMLParser()
TOTAL_DEVIATION = 0.0
MOVIE_COUNT = 0
TOTAL_RATING_REQUEST_WAIT_TIME = 0

def getAvgRating(element):
    rating = etree.fromstring(SCRAPER.get("https://letterboxd.com" + element.get("data-item-link")).text[:3456], PARSER).cssselect('meta[name="twitter:data2"]')
    return rating

async def asyncFetch(element):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, getAvgRating, element)

def processMovieTotalDeviation(movie, rating):
    global TOTAL_DEVIATION
    tijo = float(movie[0].get('content')[:4])
    print(tijo)
    TOTAL_DEVIATION += abs(rating - tijo)
    return

def incrementMovieCount():
    global MOVIE_COUNT
    MOVIE_COUNT += 1
    return

##
#takes a rated movie webpage and the rating of movies on the page
#todo needs verification it's not a timeout page
#
async def DissectMovies(movieList, rating):
    movieGrid = movieList.cssselect('ul.-p70 li .react-component')
    results = await asyncio.gather(*(asyncFetch(movie) for movie in movieGrid))
    for r in results:
        if r:
            incrementMovieCount()
            processMovieTotalDeviation(r, rating)
    # for movie in movieGrid:
    #     global TOTAL_RATING_REQUEST_WAIT_TIME
    #     requestStartTime = time.perf_counter()
    #     avgRating = getAvgRating(movie)
    #     TOTAL_RATING_REQUEST_WAIT_TIME += (time.perf_counter() - requestStartTime)
    #
    #     if avgRating:
    #         global TOTAL_DEVIATION
    #         global MOVIE_COUNT
    #         TOTAL_DEVIATION += abs(rating - float(avgRating[0].get('content')[:4]))
    #         MOVIE_COUNT += 1
    #
    #     else:
    #         print("no one watches this shit movie sorry")
    return

def HandlePagination():
    return

def main():
    ratings = [.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]

    for rating in ratings:
        ratingStartTime = time.perf_counter()
        text = SCRAPER.get("https://letterboxd.com/ralphpolojames/films/rated/" + str(rating) + "/by/rating/").text
        html_root = etree.fromstring(text, PARSER)
        asyncio.run(DissectMovies(html_root, rating))
        print("runtime for rating " + str(rating) + " is " + str(time.perf_counter() - ratingStartTime))
    return

if __name__ == '__main__':
    programStartTime = time.perf_counter()

    main()
    print(TOTAL_DEVIATION)
    print(MOVIE_COUNT)
    print(TOTAL_DEVIATION / MOVIE_COUNT)
    print("movie count: " + str(MOVIE_COUNT))
    print("program runtime:" + str(time.perf_counter() - programStartTime))
    print("average request wait time for rating pages: " + str(TOTAL_RATING_REQUEST_WAIT_TIME / MOVIE_COUNT))