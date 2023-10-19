#!/usr/bin/python3

# Import MySQL Python connector
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
import time

class Database:
    def __init__(self):
        self.host = "cpsc4910-mysql11.research.utc.edu"
        self.user = "cs4910-epb-cust-heat-remote"
        self.password = "5tvaH.epb"
        self.database = "epb_cust_htg"
        self.connection = self.connectToDB()

    def connectToDB(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def retrievePowerFromDB(self, premise):
        query = f"SELECT * FROM power_usage WHERE premise = {premise} and recorded_date > 20201231 and recorded_date < 20220101;"
        df = pd.read_sql_query(query, self.connection)
        return df

    def retrievePowerFromDBSP(self, premise):
        cursor = self.connection.cursor()
        try:
            cursor.callproc('find_power_usage_by_premise_id', [premise])
            result = cursor._stored_results[0].fetchall()
            df = pd.DataFrame(result, columns=['Date', 'Hour', 'Premise', 'Usage'])
            return df
        except mysql.connector.Error as e:
            print(e)
        

    def retrieveTempFromDB(self, premiseDF):
        dates = premiseDF.Date.unique()
        weatherData = []
        list = self.query("SELECT * FROM daily_weather;")
        temporary = []
        weatherData = []
        #TODO: Possibly expand to 2022
        for x in list:
            if(x[0].year==2021):
                temporary.append([str(x[0]).replace('-',''),x[1]])
        return temporary

    def retrieveSqFtFromDB(self, premise):
        sqft = self.query(f"select sqft from sqft where premise = {premise}")
        print(sqft)
        if (len(sqft) == 0):
            return None
        return sqft[0][0]

    def insertInference(self, predictionsDF):
        engine = create_engine(f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}/{self.database}")
        rows_affected = predictionsDF.to_sql("predictions", con=engine, if_exists='replace', index=False)
        rows_affected = rows_affected if rows_affected is not None else 0
        return rows_affected
    
    def closeConnection(self):
        if self.connection.is_connected():
            self.connection.close()

        
# Test
def main():
    db = Database()
    start_time = time.time()
    for i in range(1, 100000):
        db.retrievePowerFromDBSP(i)
    print("--- Stored Procedures: %s seconds ---" % (time.time() - start_time))


    start_time = time.time()
    for i in range(1, 100000):
        db.retrievePowerFromDB(i)
    print("--- Normal Query: %s seconds ---" % (time.time() - start_time))

