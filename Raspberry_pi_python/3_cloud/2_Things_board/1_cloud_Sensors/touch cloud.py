import os
import time
import sys
import paho.mqtt.client as mqtt
import json
import time
import RPi.GPIO as GPIO
Cloud_Host = 'XXXXXXXXXX'
ACCESS_TOKEN = 'XXXXXXXX'
# Data capture and upload interval in seconds.
sensor_data = {'pressed': '', 'count': 0}
next_reading = time.time() 
client = mqtt.Client()
# Set access token
client.username_pw_set(ACCESS_TOKEN)

client.connect(Cloud_Host, 1883, 60)
client.loop_start()
GPIO.setmode(GPIO.BCM)
Pin = 4
count=0
GPIO.setup(Pin, GPIO.IN)

try:
    while True:
        Pressed =  GPIO.input(Pin)
        if Pressed == 1:
            print "PRESSED"
            count +=1
            sensor_data['pressed'] = "Touched"
            sensor_data['count'] = count
        elif Pressed == 0:
            print "NOT PRESSED"
            count=0
            sensor_data['pressed'] = "Not Touched"
        client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
        time.sleep(2)
except KeyboardInterrupt:
    pass
client.loop_stop()
client.disconnect()
