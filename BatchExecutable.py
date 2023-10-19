# The primary executable file from which the program can be run. 

from datetime import datetime
from Database import Database
from SpikeDetector import getSpikes
from SpikeDetector import getSpikesTemp
from PlotAnalysis import dailyAverage
from PlotAnalysis import buildVisual
from PlotAnalysis import sendToOutputDB
from InferenceLogic import infer, inferCorrelation
#import pandas as pd
from mysql.connector.errors import ProgrammingError
from statistics import StatisticsError


def Main():
    '''
    isValidPremise = False
    print(datetime.now())
    prem = input("Input premise ID: ")
    # Loops until prem is a valid integer.    
    while (not isValidPremise):
        try:
            if (int(prem)):
                isValidPremise = True    
        except: 
            prem = input("Premise ID must be a integer. Please try again: ")
    print("Retrieving Premise Power Usage Data...")
    '''

    db = Database()
    if db.connection.is_connected():
        print("Connected to database")
    else:
        print("Not connected to database")
    start_time = datetime.now() # record start time
    prems = db.query("SELECT premise FROM premises;")
    premise_array = [premise[0] for premise in prems]
    tempData = []
    drops = []
    print("Starting...")
    print(len(prems))
    for prem in premise_array:
        try:
            premiseData = db.retrievePowerFromDBSP(prem) #get power usage data for given premise from utc hosted database
            if not tempData:
                tempData = db.retrieveTempFromDB(premiseData)
            print("Premise = {}".format(prem))
            #print("Retrieving Weather Data...")
            #print("Calculating Spikes/Drops...")
            averageArray = dailyAverage(premiseData)
            correlationAvg = inferCorrelation(tempData, averageArray)
            spikes = getSpikes(averageArray,410)
            if not drops:
                drops = getSpikesTemp(tempData,-410)
            #print("Building Visual...")    
            sqft = db.retrieveSqFtFromDB(prem)
            inference = infer(drops, spikes, correlationAvg, sqft)
            sendToOutputDB(prem, averageArray, inference)

            # The following lines of code are used to insert the predictions
            # Uncomment for inputting predictions into database 

            #heating_type = "Electric" if inference.get("Electric confidence:") > inference.get("Non-Electric confidence:") else "Non-Electric"
            #predictions = [[int(prem), heating_type, inference.get("Electric confidence:"), inference.get("Non-Electric confidence:")]]
            #predictionsDF = pd.DataFrame(predictions, columns=['premise', 'prediction', 'electric_confidence', 'nonelectric_confidence'])
            #rows_affected = db().insertInference(predictionsDF)


            # Uncomment if you want to print out the confidence intervals and see graph

            #print("Electric Confidence Rating: " + str(inference.get("Electric confidence:")))
            #print("Non-Electric Confidence Rating: " + str(inference.get("Non-Electric confidence:")))
            #buildVisual(tempData,averageArray,spikes,drops,inference,prem, sqft)
            
            #print("--------------------------------------------------")
            #print(datetime.now())
        except ProgrammingError as err:
            print("The premise ID: " + prem + " was not found in our database. Please try again.")
        except StatisticsError as err:
            print("There was an error with the Stats. Please try again.")
        except ValueError as errr:
            print("There was an error with the Value. Please try again.")
    db.closeConnection()
    end_time = datetime.now() # record end time
    print("Time taken:", end_time - start_time) # print time taken
Main()
