import sqlite3 as sql
import os
import json
from datetime import datetime

class database:

    def __init__(self, DB_PATH):
        self.connection = sql.connect(DB_PATH)
        self.cursor = self.connection.cursor()

    def getData(self, days='1 day'):

        # period = '-' + days
        # query = f''' SELECT * from mood where datetime('now', '{period}'); '''
        query = ''' SELECT * from mood; '''
        
        self.cursor.execute(query)

        results = self.cursor.fetchall()
        result_dict = {index : row for index, row in enumerate(results)}

        if not result_dict:
            result_dict = "No results Found"

        return json.dumps(result_dict)

    def insertData(self, data):

        data.append(1)
        data.append(':'.join(str(datetime.now()).split(":")[0:2]))      ## adding the current time

        data = tuple(data)

        query = f''' INSERT into mood (emotion, joy, fear, anger, sadness, neutral, journal, userid, journaltime)
                    VALUES {data};
                '''
        try:
            self.cursor.execute(query)
            self.connection.commit()
            print("query successful")
            return json.dumps(True)
        except Exception as e:
            print("There was an error in inserting the data \n" + str(e))
            return json.dumps(False)