import time
import json
import requests
from datetime import datetime
from store_Sensor_Data_to_DB import openweather_Data_Handler
w={"Cityname":"","Data_and_Time":"","Temperature":"","Humidity":"","Pressure":""}
api_key = "05c7f8b28705511925335e9de0c1ab9a"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city_name = 'mysore'
complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
while True:
    response = requests.get(complete_url)
    x = response.json()
    #print(x)
    y = x["main"]
    w["Data_and_Time"]=(datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
    w["Cityname"]=city_name
    w["Temperature"]=round(y["temp"]-273.15,2)
    w["Humidity"]=y["humidity"] 
    w["Pressure"]=y["pressure"]
    j=json.dumps(w)
    print(j)
    openweather_Data_Handler(j)
    time.sleep(3)
