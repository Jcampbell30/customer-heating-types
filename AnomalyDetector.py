from enum import Enum

class Anomaly:
    def __init__(self, premiseId:int, anomaly_type:int, time:str):
        self.premiseId = premiseId
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
        '''
        ZERO_USE = 1
        NEGATIVE_USE = 2


def detect_anomaly(premise_id, date, power_data, weather_data) -> Anomaly:
    if _detect_negative_use():
        return Anomaly(
            premiseId=premise_id,
            anomaly_type=Anomaly.AnomalyTypes.NEGATIVE_USE, 
            time=date
            )
    if _detect_zero_use():
        return Anomaly(
            premise_id = premise_id, 
            anomaly_type =Anomaly.AnomalyTypes.ZERO_USE,
            time= date)

def _detect_zero_use() -> bool:
    pass

def _detect_negative_use() -> bool:
    pass
