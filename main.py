from lxml import etree
from lxml.cssselect import CSSSelector
import cloudscraper
import asyncio

#GLOBAL VARIABLES
SCRAPER = cloudscraper.create_scraper(
    interpreter='js2py',        # Best compatibility for v3 challenges
    # Stealth mode
    enable_stealth=True,
    stealth_options={
        'min_delay': .1,  # Minimum delay between requests
        'max_delay': 1.2,  # Maximum delay between requests
        'human_like_delays': True,  # Use human-like delay patterns
        'randomize_headers': True,  # Randomize request headers
        'browser_quirks': True,  # Enable browser-specific quirks
        'simulate_viewport': True,  # Simulate viewport changes
        'behavioral_patterns': True  # Use behavioral pattern simulation
    },
    browser='chrome'
)
SCRAPER._max_request_depth = 500 #big uh oh no no bandaid fix todo fix
PARSER = etree.HTMLParser()
TOTAL_DEVIATION = 0.0
MOVIE_COUNT = 0
TOTAL_RATING_REQUEST_WAIT_TIME = 0

###
# retrieves and dissects the average rating for the given movie
#
# @param movie  an HTML list item of the movie to get the avgRating for
# @return       returns the average rating as a float, or returns None if the movie does not have an average rating
def getAvgRating(movie):
    ratingPairList = (etree.fromstring(SCRAPER.get("https://letterboxd.com" + movie.get("data-item-link")).text[:3456], PARSER)
                .cssselect('meta[name="twitter:data2"]'))

    # handle films without an average rating
    if not ratingPairList:
        return None

    return float(ratingPairList[0].get('content')[:4])

###
# an asynchronous wrapper for getAvgRating
#
# @param movie      an HTML list item
# @return awaitable
async def asyncFetch(movie):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, getAvgRating, movie)

###
# updates the global total deviation
#
# @param avgRating
# @param userRating
# @return void
def processMovieTotalDeviation(avgRating, userRating):
    global TOTAL_DEVIATION
    TOTAL_DEVIATION += abs(userRating - avgRating)
    return

###
# increments the global movie count
#
# @param void
# @return void
def incrementMovieCount():
    global MOVIE_COUNT
    MOVIE_COUNT += 1
    return

### todo need to verify that the webpage is not a timeout page. although have not gotten a single timeout webpage now with updated cloudflare circumvention
# For each movie, adds the count and absolute deviation to MOVIE_COUNT and TOTAL_DEVIATION respectively
#
# @param htmlRoot    the webpage that contains the moviegrid to dissect
# @param rating      the user's rating for all movies on htmlRoot
# @return void       instead just modifies the global variables MOVIE_COUNT and TOTAL_DEVIATION
async def DissectMovies(htmlRoot, userRating):
    movieGrid = htmlRoot.cssselect('ul.-p70 li .react-component')
    avgRatings = await asyncio.gather(*(asyncFetch(movie) for movie in movieGrid))
    for avgRating in avgRatings:
        if avgRating:
            incrementMovieCount()
            processMovieTotalDeviation(avgRating, userRating)
    return

def HandlePagination(htmlRoot):

    return False

def main():
    ratings = [.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    user = "jomimo"

    for rating in ratings:
        pageNo = 1
        ratingBaseUrl = "https://letterboxd.com/" + user + "/films/rated/" + str(rating) + "/by/rating/page/"

        #god forbid a language have a do while loop lmfao
        htmlRoot = etree.fromstring(SCRAPER.get(ratingBaseUrl + str(pageNo)).text, PARSER)
        asyncio.run(DissectMovies(htmlRoot, rating))
        while(HandlePagination(htmlRoot)):
            pageNo += 1
            htmlRoot = etree.fromstring(SCRAPER.get(ratingBaseUrl + str(pageNo)).text, PARSER)
            asyncio.run(DissectMovies(htmlRoot, rating))

    return

if __name__ == '__main__':

    main()
    print(TOTAL_DEVIATION)
    print(TOTAL_DEVIATION / MOVIE_COUNT)
    print("movie count: " + str(MOVIE_COUNT))