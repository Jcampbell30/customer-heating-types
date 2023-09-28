import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from sqlalchemy import create_engine
from mysql.connector.errors import InterfaceError
import mysql.connector

import sys

#method for creating a dataset of daily average with dates in the format of [date,daily average]. Returns array of these entries for the whole year
def dailyAverage(premiseDF):
    dates = premiseDF.Date.unique() #array of every unique entry in the date field of the premise dataframe, should contain each date of teh y
    averageArray = []
    for each in dates:
        df = premiseDF.loc[premiseDF['Date'] == each]
        dailyAverageUsage = df["Usage"].mean()
        averageArray.append([each,dailyAverageUsage])
    return averageArray

def sendToOutputDB(premise, weather, power):
    
    # CONNECT TO DB
    # TODO: Redo database class to allow more flexible database entry
    mydb = mysql.connector.connect(
    host="cpsc4910-mysql11.research.utc.edu",
    user="cs4910-epb-cust-heat-remote",
    password="5tvaH.epb",
    database="output_db"
    )
    cursorObject = mydb.cursor()

    # PROCESS DATA FOR DB
    data : dict = {}

    for each in weather:
        data[f'{each[0]}'] = {'weather' : each[1]}
    for each in power:
        data[f'{each[0]}']['power'] = each[1]
    
    formatted_data = []
    for date, value in data.items():
        try:
            formatted_data.append(tuple([premise, date, value['power']]))
        except:
            pass

    try:
        query = f'INSERT IGNORE INTO power_data(premise_id, data_date, power_data) VALUES (%s, %s, %s);'
        cursorObject.executemany(query, formatted_data)
        mydb.commit()
    except InterfaceError as err:
        print(err)
    except :
        raise Exception(f'Cannot insert power data into table for premise <{premise}>. Error: {sys.exc_info()[0]}')
    
    mydb.close()

#method for creating the matplot visual, powerSpikes and tempDrops parameters optional. IF included they spikes/drops will be shown on the visual. If not, only the usage and temp lines will be plotted
def buildVisual(weather,power,powerSpikes = None,tempDrops = None, inference = None, premise = None, sqft = None):
    weatherData = []
    powerData = []
    
    for each in weather:
        weatherData.append(each[1])
    for each in power:
        powerData.append(each[1])
    
    rc('mathtext', default='regular')
    # Generating power consumption dataset
    x = np.arange(365)

    # Creating figure
    fig = plt.figure()

    # Plotting weather data
    ax = fig.add_subplot(111)
    ax.plot(x, weatherData, '-b', label='Temp')

    # Creating Twin axes for power data
    ax2 = ax.twinx()
    ax2.plot(x, powerData, '-r', label='Power')

    # Adding title
    title = f"Temperature vs. Power Consumption with Sqft: {sqft}" if sqft is not None else 'Temperature vs. Power Consumption'
    plt.title(title, fontweight="bold")

    # Adding legend
    ax.legend(loc=2)
    ax2.legend(loc=0)

    # Adding grid
    ax.grid()

    # Adding labels
    ax.set_xlabel("Time")
    ax.set_ylabel(r"Temperature (Celsius)")
    ax2.set_ylabel(r"Power consumption (kWh)")

    # Setting tick labels
    labels = ['Jan '+str(2021), 'Feb', 'March', 'April', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec', 'Jan '+str(2022)]
    ax2.set_xticks([0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 365])
    ax2.set_xticklabels(labels)

    # Setting Y limits
    ax2.set_ylim(0, 5) # right axis
    ax.set_ylim(-5, 35) # left axis

    # Show plot
    plt.rc('font', size=30)
    plt.rc('xtick', labelsize=30)
    plt.rc('ytick', labelsize=30)
    plt.rc('axes', labelsize=20)
    
    if(inference != None):
        electricRate = inference["Electric confidence:"]
        nonElectricRate = inference["Non-Electric confidence:"]
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(0.05, 0.95, "Premise ID: "+ str(premise) + "\n" + "Electric Confidence Rating: " + str(electricRate) + "\n" + "Non-Electric Confidence Rating: " + str(nonElectricRate) , transform=ax.transAxes, fontsize=16, verticalalignment='top', bbox=props)
    
    if(powerSpikes != None):
        spikes = []
        for each in powerSpikes: spikes.append(each[1])
        arr = []
        for each in spikes:
            index = int(powerData.index(each))
            arr.append(index)
        plt.plot(arr,spikes,'o', color='r',  markersize=8)

    if(tempDrops != None):
        drops = []
        for each in tempDrops: 
            drops.append(each[1]) 
        
        arr = []
        for each in drops:
            index = int(weatherData.index(each))
            arr.append(index)
        ax.plot(arr,drops,'o', color='b',  markersize=8)
    plt.show()
    plt.close() 
