

import paho.mqtt.client as mqtt
import random, threading, json
from datetime import datetime


#====================================================
# MQTT Settings 
MQTT_Broker = "broker.hivemq.com"
MQTT_Port = 1883
Keep_Alive_Interval = 45

Mqtt="iot/python/sensordata"

#====================================================


                
mqttc = mqtt.Client()

print(mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))     )       

                
def publish_To_Topic(topic, message):
        mqttc.publish(topic,message)
        print ("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
        print ("")


#====================================================
# FAKE SENSOR 
# Dummy code used as Fake Sensor to publish some random values
# to MQTT Broker

toggle = 0

def publish_Fake_Sensor_Values_to_MQTT():
        threading.Timer(2.0, publish_Fake_Sensor_Values_to_MQTT).start()
        Temperature_Fake_Value = float("{0:.2f}".format(random.uniform(1, 30)))
        Temperature_Fake_Value_far = float("{0:.2f}".format(random.uniform(60, 90)))
        Humidity_Fake_Value = float("{0:.2f}".format(random.uniform(50, 100)))
        sensordata = {}
        sensordata['Sensor_ID'] = "DHT11"
        sensordata['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
        sensordata['Temperature'] = Temperature_Fake_Value
        sensordata['Humidity'] = Humidity_Fake_Value
        sensordata['Temperature_far'] = Temperature_Fake_Value_far   
        temperature_json_data = json.dumps(sensordata)                                                                        
        print( "Publishing fake Temperature Value: " + str(sensordata) + "...")
        publish_To_Topic (Mqtt, temperature_json_data)                                                                        
        toggle = 0
                                                                                


publish_Fake_Sensor_Values_to_MQTT()

#====================================================
