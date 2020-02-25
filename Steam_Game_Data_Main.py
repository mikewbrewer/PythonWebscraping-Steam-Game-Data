from Steam_Game_Data_Extraction import extractDataFromSteam
from Steam_Game_Data_Analytics import addDataToSheets



def runEverything():
    extractDataFromSteam()
    addDataToSheets()



if __name__ == '__main__':
    runEverything()
