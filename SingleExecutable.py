# The primary executable file from which the program can be run. 

from datetime import datetime
from Database import Database as db
from SpikeDetector import getSpikes as getSpikes
from SpikeDetector import getSpikesTemp as getSpikesTemp
from PlotAnalysis import dailyAverage as dailyAverage
from PlotAnalysis import buildVisual as buildVisual
from InferenceLogic import infer, inferCorrelation
import pandas as pd
from mysql.connector.errors import ProgrammingError
from statistics import StatisticsError


def Main():
    isValidPremise = False
    print(datetime.now())
    premiseId = input("Input premise ID: ")

    # Loops until premiseId is a valid integer.    
    while (not isValidPremise):
        try:
            if (int(premiseId)):
                isValidPremise = True    
        except: 
            premiseId = input("Premise ID must be a integer. Please try again: ")
    
    print("Retrieving Premise Power Usage Data...")
    try:
        premiseData = db().retrievePowerFromDB(premiseId) #get power usage data for given premise from utc hosted database
        print("Retrieving Weather Data...")
        tempData = db().retrieveTempFromDB(premiseData)
        print("Calculating Spikes/Drops...")
        averageArray = dailyAverage(premiseData)
        spikes = getSpikes(averageArray,410)
        drops = getSpikesTemp(tempData,-410)
        print("Building Visual...")
        correlationAvg = inferCorrelation(tempData,averageArray)
        sqft = db().retrieveSqFtFromDB(premiseId)
        inference = infer(drops, spikes, correlationAvg, sqft)
        print("Electric Confidence Rating: " + str(inference.get("Electric confidence:")))
        print("Non-Electric Confidence Rating: " + str(inference.get("Non-Electric confidence:")))
        buildVisual(tempData,averageArray,spikes,drops,inference,premiseId, sqft)
        heating_type = "Electric" if inference.get("Electric confidence:") > inference.get("Non-Electric confidence:") else "Non-Electric"
        predictions = [[int(premiseId), heating_type, inference.get("Electric confidence:"), inference.get("Non-Electric confidence:")]]
        predictionsDF = pd.DataFrame(predictions, columns=['premise', 'prediction', 'electric_confidence', 'nonelectric_confidence'])
        rows_affected = db().insertInference(predictionsDF)
        print(datetime.now())
    except ProgrammingError as err:
        print("The premise ID: " + premiseId + " was not found in our database. Please try again.")
    except (StatisticsError, ValueError) as err:
        print("There was an error with the results. Please try again.")
    
Main()
