import paho.mqtt.client as paho
import time
import json
import requests
api_key = "05c7f8b28705511925335e9de0c1ab9a"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

city_name = 'Bangalore'
complete_url = base_url + "appid=" + api_key + "&q=" + city_name 

def on_connect(client, userdata, rc):
    print("Connection returned result: "+connack_string(rc))
 
def on_publish(client, userdata, mid):
    print("mid: "+str(mid))
    print("client: "+str(client))
    print("userdata: "+str(userdata))
    print ("Message Published...")
 
ACCESS_TOKEN = '3Jxx0tuzo3B01FRUyyDm'


 
client = paho.Client()
client.on_publish = on_publish
client.username_pw_set(ACCESS_TOKEN)
client.connect("demo.thingsboard.io", 1883)
client.loop_start()
w={"TEMP":"","HUM":"","PRESSURE":""}
while True:
    response = requests.get(complete_url)
    x = response.json()
    print(x)
    y = x["main"] 
    w["TEMP"]=y["temp"]-273.15
    w["HUM"]= y["humidity"]   
    w["PRESSURE"]=y["pressure"]
    (rc, mid) = client.publish("v1/devices/me/telemetry", json.dumps(w), qos=1)
    print (rc)
    print (mid)
    time.sleep(1)
