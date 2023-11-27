from enum import Enum

class Anomaly:
    def __init__(self, premise_id:int, anomaly_type:int, time:str):
        self.premise_id = premise_id
        self.anomaly_type = anomaly_type
        self.time = time

    def __str__(self):
        return "Premise ID: " + str(self.premiseId) + " Anomaly: " + str(self.anomaly_type) + " Time: " + str(self.time)
    
    class AnomalyTypes(Enum):
        '''
        #############################
        # ANOMALY TYPE EXPLANATIONS #
        #############################

        ZERO_USE        : The power data for a given premise shows zero power usage.
        NEGATIVE_USE    : The power data for a given premise shows negative power usage.
        NON_CONFIDENCE  : The power data for a given premise has low confidence.
        '''
        ZERO_USE = 1
        NEGATIVE_USE = 2
        NON_CONFIDENCE = 3


def detect_anomaly(premise_id : int, power_data : list, weather_data : list, confidence_rating : float) -> list:
    """Detects all of the anomalies attached to an individual residence then returns them all.

    Args:
        premise_id (int): The ID for a premise in the database.
        power_data (list): A list containing all of the power usage data on a per-day basis for a premise.
        weather_data (list): A list containing all of the weather data on a per-day basis.
        confidence_rating (float): A float representing the confidence rating for a given premise.

    Returns:
        list: A list of all the anomalies detected for a given premise.
    """    

    detected_anomalies : list = []

    # Check for zero power use situations.
    zero_use_check : dict = _detect_zero_use(power_data)
    if zero_use_check['is_detected'] == True:
        for each in zero_use_check['anomalies']:
            detected_anomalies.append(Anomaly(
                premise_id = premise_id, 
                #anomaly_type =Anomaly.AnomalyTypes.ZERO_USE,
                anomaly_type = 1,
                time=each))
    
    # Check for negative power use situations.
    negative_use_check : dict = _detect_negative_use(power_data)
    if negative_use_check['is_detected'] == True:
        for each in negative_use_check['anomalies']:
            detected_anomalies.append(Anomaly(
                premise_id=premise_id,
                #anomaly_type=Anomaly.AnomalyTypes.NEGATIVE_USE,
                anomaly_type = 2, 
                time=each))
            
    # Check for low confidence.
    if _detect_non_confidence(confidence_rating):
        detected_anomalies.append(Anomaly(
            premise_id=premise_id,
            anomaly_type= 3,
            time=1
        ))
    
    return detected_anomalies


def _detect_zero_use(power_data : list) -> dict:
    data : dict = {}
    data['is_detected'] = False
    data['anomalies'] = []
    for each in power_data:
        date = each[0]
        power = each[1]
        if power == 0:
            data['is_detected'] = True
            month = _parse_date_for_month(date)
            if month not in data['anomalies']:
                data['anomalies'].append(month)

    return data

def _detect_negative_use(power_data : list) -> dict:
    data: dict = {}
    data['is_detected'] = False
    data['anomalies'] = []
    for each in power_data:
        date = each[0]
        power = each[1]
        if power < 0:
            data['is_detected'] = True
            month = _parse_date_for_month(date)
            if month not in data['anomalies']:
                data['anomalies'].append(month)
    
    return data

def _detect_non_confidence(confidence_rating : float) -> bool:
    if confidence_rating > 70 or confidence_rating < 50:
        return False
    return True

def _parse_date_for_month(date:str) -> int:
    #20210108   >>>   01s
    date = str(date)
    new_date = f'{date[0]}{date[1]}{date[2]}{date[3]}{date[4]}{date[5]}01'
    return int(new_date)