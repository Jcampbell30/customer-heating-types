#!/usr/bin/python3

# Import MySQL Python connector
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
import time

class Database:

    host = "cpsc4910-mysql11.research.utc.edu"
    user = "cs4910-epb-cust-heat-remote"
    password = "5tvaH.epb"
    database = "epb_cust_htg"

    def connectToDB(self):
        # Connect to database on MySQL Linux Server
        # TODO: add environment variables
        mydb = mysql.connector.connect(
        host="cpsc4910-mysql11.research.utc.edu",
        user="cs4910-epb-cust-heat-remote",
        password="5tvaH.epb",
        database="epb_cust_htg"
        )
        cursorObject = mydb.cursor()
        return cursorObject, mydb

    # General function for querying data
    # TODO: Maybe some kind of input validation, either in this file or outside
    def query(self, query):
        cursorObject,mydb = self.connectToDB()
        cursorObject.execute(query)
        result = cursorObject.fetchall()
        mydb.close()
        return result

    def retrievePowerFromDB(self, premise):
        list = Database().query("SELECT * FROM power_usage WHERE premise = "+str(premise)+" and recorded_date > 20201231 and recorded_date < 20220101;")
        df = pd.DataFrame(list,columns=['Date','Hour','Premise','Usage'])
        return df

    # Stored procedure database call
    def retrievePowerFromDBSP(self, premise):
        cursorObject,mydb = self.connectToDB()
        try:
            cursorObject.callproc('find_power_usage_by_premise_id', [premise])
            list = cursorObject._stored_results[0].fetchall()

            df = pd.DataFrame(list,columns=['Date','Hour','Premise','Usage'])
            return df

        except mysql.connector.Error as e:
            print(e)

        finally:
            cursorObject.close()
            mydb.close()


    def retrieveTempFromDB(self, premiseDF):
        dates = premiseDF.Date.unique()
        weatherData = []
        list = Database().query("SELECT * FROM daily_weather;")
        temporary = []
        weatherData = []
        #TODO: Possibly expand to 2022
        for x in list:
            if(x[0].year==2021):
                temporary.append([str(x[0]).replace('-',''),x[1]])
        return temporary

    def retrieveSqFtFromDB(self, premise):
        sqft = self.query(f"select sqft from sqft where premise = {premise}")
        if (len(sqft) == 0):
            return None
        return sqft[0][0]

    def insertInference(self, predictionsDF):
        engine = create_engine(f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}/{self.database}")
        rows_affected = predictionsDF.to_sql("predictions", con=engine, if_exists='replace', index=False)
        rows_affected = rows_affected if rows_affected is not None else 0
        return rows_affected

        
# Test
def main():
    start_time = time.time()
    for i in range(1, 100000):
        Database().retrievePowerFromDBSP(i)
    print("--- Stored Procedures: %s seconds ---" % (time.time() - start_time))


    start_time = time.time()
    for i in range(1, 100000):
        Database().retrievePowerFromDB(i)
    print("--- Normal Query: %s seconds ---" % (time.time() - start_time))