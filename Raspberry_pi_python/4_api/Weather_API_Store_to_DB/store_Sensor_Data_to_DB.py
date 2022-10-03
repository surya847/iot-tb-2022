
import json
import sqlite3

# SQLite DB Name
DB_Name =  "Weather-DB.db"

#===============================================================
# Database Manager Class

class DatabaseManager():
	def __init__(self):
		self.conn = sqlite3.connect(DB_Name)
		self.conn.execute('pragma foreign_keys = on')
		self.conn.commit()
		self.cur = self.conn.cursor()
		
	def add_del_update_db_record(self, sql_query, args=()):
		self.cur.execute(sql_query, args)
		self.conn.commit()
		return

	def __del__(self):
		self.cur.close()
		self.conn.close()

#===============================================================
# Functions to push Sensor Data into Database

# Function to save Temperature to DB Table
def Weather_Data_Handler(jsonData):
        global ph
        json_Dict = json.loads(jsonData)
        Cityname = json_Dict['Cityname']
        Date_n_Time = json_Dict['Data_and_Time']
        Temperature = json_Dict['Temperature']
        Humidity = json_Dict['Humidity']
        Pressure=json_Dict['Pressure']
        dbObj = DatabaseManager()
        dbObj.add_del_update_db_record("insert into Weather_table(Cityname, Date_n_Time, Temperature,Humidity ,Pressure) values (?,?,?,?,?)",[Cityname, Date_n_Time, Temperature,Humidity,Pressure])
        del dbObj
        print( "Inserted Sensor Data into Database.")
        print ("")

#===============================================================
# Master Function to Select DB Funtion based on MQTT Topic

def openweather_Data_Handler(jsonData):
        Weather_Data_Handler(jsonData)
	

#===============================================================
