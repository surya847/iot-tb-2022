import sqlite3

# SQLite DB Name
DB_Name =  "Weather-DB.db"

# SQLite DB Table Schema
TableSchema="""
drop table if exists Weather_table ;
create table Weather_table (
  id integer primary key autoincrement,
  Cityname text,
  Date_n_Time text,
  Temperature text,
  Humidity text,
  Pressure text
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
