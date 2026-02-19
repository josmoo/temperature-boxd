from lxml import etree
from lxml.cssselect import CSSSelector
import cloudscraper
import asyncio

import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.set_global_font_scale(1.6)
########
#GLOBAL#
########
CONTENT_WIDTH = 344
TOTAL_DEVIATION = 0.0
MOVIE_COUNT = 0
PARSER = etree.HTMLParser()
SCRAPER = cloudscraper.create_scraper(
    interpreter='js2py',
    enable_stealth=True,
    stealth_options={
        'min_delay': .05,
        'max_delay': .35,
        'human_like_delays': True,
        'randomize_headers': True,
        'browser_quirks': True,
        'simulate_viewport': True,
        'behavioral_patterns': True
    },
    browser='chrome'
)
SCRAPER._max_request_depth = 500 #big uh oh no no bandaid fix todo fix

class RatingsNotFound(Exception):
    def __init__(self, username):
        super.__init__("Could not find any move ratings for: " + username)
        self.username = username

###
# gets the total number of movies the user has rated
#
# @param user
# @return int
# @raise RatingsNotFound
def getRatedMovieCount(user):
    abc = (etree.fromstring(SCRAPER.get("https://letterboxd.com/" + user).text, PARSER)).cssselect('.cols-2 > .wide-sidebar > .ratings-histogram-chart > .all-link')
    if(abc):
        return int(abc[0].text.replace(',', ''))
    raise RatingsNotFound(user)

###
# updates progress bar UI object
#
# @param ratedMovies    the amount of movies we have calculated the MAD for so far
# @return void
def updateProgressBar(ratedMovies):
    progress = MOVIE_COUNT / ratedMovies
    dpg.set_value("Progress Bar",   progress)
    dpg.configure_item("Progress Bar", overlay=f"{100*progress:.2f}%")
    return

###
# the real "main" function. takes the letterboxd username from the UI field and collects the MAD for each movie,
#   and displays progress and results to UI
#
# @return void
def calculateTemperature():
    user = dpg.get_value("Username Field")
    try:
        ratedMovies = getRatedMovieCount(user)
    except RatingsNotFound:
        return

    dpg.show_item("Progress Bar")
    ratings = [.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]

    for rating in ratings:
        pageNo = 1
        ratingBaseUrl = "https://letterboxd.com/" + user + "/films/rated/" + str(rating) + "/by/rating/page/"

        # god forbid a language have a do while loop lmfao
        htmlRoot = etree.fromstring(SCRAPER.get(ratingBaseUrl + str(pageNo)).text, PARSER)
        asyncio.run(dissectMovies(htmlRoot, rating))
        updateProgressBar(ratedMovies)
        while (handlePagination(htmlRoot)):
            pageNo += 1
            htmlRoot = etree.fromstring(SCRAPER.get(ratingBaseUrl + str(pageNo)).text, PARSER)
            asyncio.run(dissectMovies(htmlRoot, rating))
            updateProgressBar(ratedMovies)

    dpg.set_value("MAD Text", "Your mean average deviation is:\n" + str(TOTAL_DEVIATION / MOVIE_COUNT))
    dpg.show_item("MAD Text")
    return

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
# @param movie  an HTML list item
# @return       awaitable that will contain the avgRating or None
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
async def dissectMovies(htmlRoot, userRating):
    movieGrid = htmlRoot.cssselect('ul.-p70 li .react-component')
    avgRatings = await asyncio.gather(*(asyncFetch(movie) for movie in movieGrid))
    for avgRating in avgRatings:
        if avgRating:
            incrementMovieCount()
            processMovieTotalDeviation(avgRating, userRating)
    return

###
# Checks if there is another page of movies to rate
#
# @param htmlRoot   the current page of movies
# @return bool      true if there is another page of movies to rate, false if there isn't
def handlePagination(htmlRoot):
    cssQueryResults = htmlRoot.cssselect('.pagination > .paginate-nextprev > .next')
    if(cssQueryResults):
        if(cssQueryResults[0].get('href')):
            return True
    return False

def main():
    with dpg.window(tag="Primary Window"):
        dpg.add_text("Enter your Letterboxd username:")
        dpg.add_input_text(tag="Username Field",
                           hint="username",
                           width=CONTENT_WIDTH,
                           no_spaces=True,
                           on_enter=True, callback=calculateTemperature)
        dpg.add_button(label="Calculate temperature",
                       callback=calculateTemperature)
        dpg.add_progress_bar(tag="Progress Bar",
                             default_value=0.0,
                             overlay="0%",
                             width=344,
                             parent="Primary Window",
                             show=False)
        dpg.add_text("",
                     tag ="MAD Text",
                     show=False)

    dpg.create_viewport(title="Temperature Boxd",
                        width=360, height=256, resizable= False,
                        small_icon="./img/temperatureBoxdFavicon.ico",
                        large_icon="./img/temperatureBoxdFavicon.ico")
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()
    return

if __name__ == '__main__':

    main()