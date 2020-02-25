import requests
import pandas as pd

from time import sleep
from random import randint
from bs4 import BeautifulSoup


def extractDataFromSteam():
    # all the files that will be written to
    files = ["Steam Game Data - Action",
        "Steam Game Data - Adventure",
        "Steam Game Data - Casual",
        "Steam Game Data - Indie",
        "Steam Game Data - Massively Multiplayer",
        "Steam Game Data - Racing",
        "Steam Game Data - RPG",
        "Steam Game Data - Simulation",
        "Steam Game Data - Sports",
        "Steam Game Data - Strategy"]

    # the url's correcspond to the filenames above
    urls = ['https://store.steampowered.com/search/?tags=19&filter=topsellers&page=',
        'https://store.steampowered.com/search/?tags=21&filter=topsellers&page=',
        'https://store.steampowered.com/search/?tags=597&filter=topsellers&page=',
        'https://store.steampowered.com/search/?tags=492&filter=topsellers&page=',
        'https://store.steampowered.com/search/?tags=128&filter=topsellers&page=',
        'https://store.steampowered.com/search/?tags=699&filter=topsellers&page=',
        'https://store.steampowered.com/search/?tags=122&filter=topsellers&page=',
        'https://store.steampowered.com/search/?tags=599&filter=topsellers&page=',
        'https://store.steampowered.com/search/?tags=701&filter=topsellers&page=',
        'https://store.steampowered.com/search/?tags=9&filter=topsellers&page=']

    # for the final export to csv files
    output_files = ['Steam_Game_Data_Action.csv',
        'Steam_Game_Data_Adventure.csv',
        'Steam_Game_Data_Casual.csv',
        'Steam_Game_Data_Indie.csv',
        'Steam_Game_Data_MassivelyMultiplayer.csv',
        'Steam_Game_Data_Racing.csv',
        'Steam_Game_Data_RPG.csv',
        'Steam_Game_Data_Simulation.csv',
        'Steam_Game_Data_Sports.csv',
        'Steam_Game_Data_Strategy.csv']


    # to keep track of the url array index as it corresponds to the correct file
    url_count = -1

    # page number
    pages = [str(i) for i in range (1, 5)]

    for filename in output_files:
        # use if connecting directly to Google Sheets
        #sheet = client.open(filename).sheet1

        # set up data arrays
        game_titles = []
        game_prices = []
        game_discount_prices = []
        game_release_dates = []
        url_count = url_count + 1

        for page in pages:
            # URL for action games
            my_url = urls[url_count]+page

            # add time between requests
            sleep(randint(8, 15))

            # set up html link with BeautifulSoup
            page = requests.get(my_url)
            soup = BeautifulSoup(page.content, 'html.parser')

            # container for all games on given page
            games_list = soup.find(id='search_resultsRows')
            game_container = games_list.findAll("div", {"class":"responsive_search_name_combined"})

            # exctract prices
            for game in game_container:
                price_container = game.find("div", {"class": "col search_price_discount_combined responsive_secondrow"})
                if (price_container.find("div", {"class": "col search_price discounted responsive_secondrow"})):
                    temp = price_container.find("div", {"class": "col search_price discounted responsive_secondrow"}).text.strip()
                    temp2 = temp.rsplit('$', 1)
                    price = temp2[0]
                    price2 = temp2[1]
                else:
                    price = price_container.text.strip()
                    price2 = ""
                game_prices.append(price)
                game_discount_prices.append(price2)

                # exctract and add titles and release dates to corresponding arrays
                game_titles.append(game.find(class_='title').get_text())
                game_release_dates.append(game.find(class_='col search_released responsive_secondrow').get_text())


        output_data = pd.DataFrame(
            {
            'Title': game_titles,
            'Price': game_prices,
            'Discount': game_discount_prices,
            'Released': game_release_dates
            })

        output_data.to_csv(filename)

if __name__ == '__main__':
    extractDataFromSteam()
