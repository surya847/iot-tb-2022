import sqlite3

# SQLite DB Name
DB_Name =  "IoT-DB.db"

# SQLite DB Table Schema
TableSchema="""
drop table if exists DHT22_Temperature_Data ;
create table DHT22_Temperature_Data (
  id integer primary key autoincrement,
  SensorID text,
  Date_n_Time text,
  Temperature text,
  Humidity text,
  Temperature_far text
);"""

#Connect or Create DB File
conn = sqlite3.connect(DB_Name)
curs = conn.cursor()

#Create Tables
sqlite3.complete_statement(TableSchema)

print(curs.executescript(TableSchema))

#Close DB
curs.close()
conn.close()
