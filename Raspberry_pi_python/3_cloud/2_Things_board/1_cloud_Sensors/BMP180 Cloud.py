import os
import time
import sys
import paho.mqtt.client as mqtt
import json
import Adafruit_BMP.BMP085 as BMP085

Cloud='XXXXXXXXXXXX'
token = 'XXXXXXXXXX'

sensor_data = {'temperature': 0, 'Pressure': 0, 'Altitute' : 0, 'Sea Level Pressure': 0}
client = mqtt.Client()

client.username_pw_set(token)
client.connect(Cloud, 1883, 60)
client.loop_start()
sensor = BMP085.BMP085()

try:
        while True:
                temp = sensor.read_temperature()
                Pressure = sensor.read_pressure()
                Altitute = sensor.read_altitude()
                Altitute = round (Altitute,2)
                sea = sensor.read_sealevel_pressure()
                print('Temp = {0:0.2f} *C'.format(sensor.read_temperature()))
                print('Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()))
                print('Altitude = {0:0.2f} m'.format(sensor.read_altitude()))
                print('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()))
                sensor_data['temperature'] = temp
                sensor_data['Pressure'] = Pressure
                sensor_data['Altitute'] = Altitute
                sensor_data['Sea Level Pressure'] = sea
                client.publish('v1/devices/me/telemetry',json.dumps(sensor_data),1)
                time.sleep(2)
                
except KeyboardInterrupt:
        pass
client.loop_stop()
client.disconnect()
