import statistics
import datetime

#method for detecting spikes (or dips) within a dataset. A data set should be an array where each entry consist of an item like: [date,usage] or [date,temp]
def getSpikes(dataset,per):
    values = []
    spikeArray = []
    for each in dataset: values.append(each[1]) #creation of a temp dataset just for calculating stdev and average for the given set
    datasetSTDev = statistics.stdev(values)
    datasetAverage =  statistics.mean(values)
    
    if(per > 0): #if the per value is positive, and we are looking for spikes
        for element in dataset:
            if datasetAverage + float(element[1]) >= datasetAverage + (per/100)*datasetSTDev: #checks if the given datapoint/value is greater than the percentage of a stdev above the average
                spikeArray.append(element)
    elif(per < 0): #if the per value is negative, and we are looking for dips
        for element in dataset:
            if float(element[1]) - datasetAverage  <= datasetAverage + (per/100)*datasetSTDev: #checks if the given datapoint/value is less than the percentage of a stdev below the average
                spikeArray.append(element)
    return spikeArray #return an array containing each instance of a spike or dip within the dataset in [data,usage] or [data,temp] format.

def getSpikesTemp(dataset,per):
    values = []
    spikeArray = []
    for each in dataset:
        if each[1] < 15.6:
            values.append(each[1])
        
    # Calculate standard deviation and average for the filtered dataset
    datasetSTDev = statistics.stdev(values)
    datasetAverage = statistics.mean(values)
    #return values
    #'''
    if(per > 0): #if the per value is positive, and we are looking for spikes
        for element in dataset:
            if element[1] < 15.6:
                if datasetAverage + float(element[1]) >= datasetAverage + (per/100)*datasetSTDev: #checks if the given datapoint/value is greater than the percentage of a stdev above the average
                    spikeArray.append(element)
    elif(per < 0): #if the per value is negative, and we are looking for dips
        for element in dataset:
            if element[1] < 15.6:
                if float(element[1]) < 15.6 and float(element[1]) - datasetAverage  <= datasetAverage + (per/100)*datasetSTDev: #checks if the given datapoint/value is less than the percentage of a stdev below the average
                    spikeArray.append(element)
    return spikeArray #return an array containing each instance of a spike or dip within the dataset in [data,usage] or [data,temp] format.
    #'''