import os
import time
import sys
import Adafruit_DHT as dht
import paho.mqtt.client as mqtt
import json

Cloud_HOST = 'XXXXXXXXXXXXX'
ACCESS_TOKEN = 'XXXXXXXXXXX'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.

INTERVAL=2
sensor_data = {'temperature': 0, 'humidity': 0}
next_reading = time.time() 
client = mqtt.Client()

# Set access token

client.username_pw_set(ACCESS_TOKEN)

# Connect to Cloud using default MQTT port and 60 seconds 
client.connect(Cloud_HOST, 1883, 60)
client.loop_start()
try:
    while True:
        humidity,temperature = dht.read_retry(dht.DHT11, 4)
        humidity = round(humidity, 2)
        temperature = round(temperature, 2)
        print(u"Temperature: {:g}*C, Humidity: {:g}%".format(temperature, humidity))
        sensor_data['temperature'] = temperature
        sensor_data['humidity'] = humidity
        # Sending humidity and temperature data to Cloud
        client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
        time.sleep(INTERVAL)
except KeyboardInterrupt:
    pass
client.loop_stop()
client.disconnect()
