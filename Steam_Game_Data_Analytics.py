import gspread
import pandas
import re

from datetime import date
from oauth2client.service_account import ServiceAccountCredentials


def addDataToSheets():
    scope = [ "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"]

    # connect to google sheets
    creds = ServiceAccountCredentials.from_json_keyfile_name("Google_Credentials.json", scope)
    client = gspread.authorize(creds)

    filename = "Steam_Game_Analytics_Data"

    sh = client.open_by_url('https://docs.google.com/spreadsheets/d/17qZwifMUgG9kqotUgCos8Z0qNhpQQulpNMvl-EaXGL0/edit#gid=0')
    worksheet = sh.get_worksheet(0)

    csv_files = ['CSVs/Steam_Game_Data_Action.csv',
        'CSVs/Steam_Game_Data_Adventure.csv',
        'CSVs/Steam_Game_Data_Casual.csv',
        'CSVs/Steam_Game_Data_Indie.csv',
        'CSVs/Steam_Game_Data_MassivelyMultiplayer.csv',
        'CSVs/Steam_Game_Data_Racing.csv',
        'CSVs/Steam_Game_Data_RPG.csv',
        'CSVs/Steam_Game_Data_Simulation.csv',
        'CSVs/Steam_Game_Data_Sports.csv',
        'CSVs/Steam_Game_Data_Strategy.csv']


    price_averages = []

    for input_file in csv_files:
        df = pandas.read_csv(input_file)
        temp_total = 0

        for index, row in df.iterrows():
            # get price on that row
            if (row['Price'] == 'Free'):
                temp = 0
            else:
                temp = str(row['Price'])
                temp = temp[1:]

            if (re.search("[0-9]$", temp)):
                temp_total = temp_total + float(temp)

        price_averages.append(temp_total / 100)

    # format the prices in a neat and tidey way
    for i in range (0, 10):
        price_averages[i] = str(round(price_averages[i], 2))

    new_row = [str(date.today())] + price_averages

    # write the data to the Google Sheet
    worksheet.append_row(new_row, 2)

if __name__ == '__main__':
    addDataToSheets()
