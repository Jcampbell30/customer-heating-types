import pandas as pd
# Method for interperating the spikes (or dips) using an estimated range. 
    # 0 to 2 correlating spikes = no significant relation
    # 3 to 5 correlating spikes = a relation present
    # > 5   correlating spikes = a significant relation
# get spikes for weather data and also for power consumption. If the dates are the
    # same, then increment the inference prediction

# TODO: Potentially account for summer months
def infer(weatherSpikes, powerSpikes, corr_coeff, sqft = None):
    intersectLength = 0 # set(weatherSpikes)&set(powerSpikes)
    weatherDates = []
    powerDates = []
    for listy in weatherSpikes:
        weatherDates.append(int(listy[0]))
    for listy in powerSpikes:
        powerDates.append(listy[0])
    intersect =  set(weatherDates).intersection(powerDates)
    intersectLength = len(intersect)

    # Added count of non-correlating spikes since this can help
    # us to determine if there are spikes happening regardless of weather
    noncorrelated_spikes = [date for date in powerDates if date not in intersect]
    correlated_to_noncorrelated_ratio = intersectLength/len(noncorrelated_spikes) if len(noncorrelated_spikes) != 0 else 0
    return inferDynamic(len(weatherDates), intersectLength, correlated_to_noncorrelated_ratio, corr_coeff, sqft)

# This method gives a more dynamically accurate interpretation by checking the percentage of intersection
# NOTE: The more significant the relation between power spikes on weather dates, the better percentage this gives.
def inferDynamic(weatherDatesLength, intersectLength, ratio, corr_coeff, sqft = None):
    rawElectricPercentage = intersectLength / float(weatherDatesLength)

    #electricPercentage = round(rawElectricPercentage * 100, 2)
    #nonElectricPercentage = abs(100 - electricPercentage)

    # Changing how electric confidence interval is calculate
    # It now starts as the absolute value of the correlation coefficent 
    # and then gets pulled either more or less confident based on the ratio
    # of correlating-to-noncorrelating spikes
    electricPercentage = round(abs(corr_coeff) * 100, 2)
    if ratio >= .10:
        electricPercentage = round(electricPercentage + ratio * 5, 2)
    elif ratio < .10:
        electricPercentage = round(electricPercentage - ratio * 5, 2)
    
    if electricPercentage > 100: electricPercentage = 100
    nonElectricPercentage = round(100 - electricPercentage, 2)
    if sqft is not None:
        print(f"Square Footage: {sqft}")
    inferencePredicition = {"Electric confidence:": electricPercentage, "Non-Electric confidence:": nonElectricPercentage}
    return inferencePredicition

#Brandon Case
#Date: 4/4/23
#Change: added method below to calculate the average correlation coefficient
def inferCorrelation(tempData, powerData):
    tempdf = pd.DataFrame(tempData, columns= ['date', 'tempC'])
    tempdf['date'] = tempdf['date'].astype(int)
    powerdf = pd.DataFrame(powerData, columns= ['date', 'power'])
    powerdf['date'] = powerdf['date'].astype(int)
    merged_df = pd.merge(tempdf, powerdf, on='date')
    #filter out temperature 60F and above.
    filtered_df = merged_df[merged_df['tempC'] < 15.6]
    corr = filtered_df['power'].corr(filtered_df['tempC'])
    return corr