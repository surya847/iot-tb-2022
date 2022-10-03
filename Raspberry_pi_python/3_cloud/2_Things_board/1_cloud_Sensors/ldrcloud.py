import os
import time
import sys
import paho.mqtt.client as mqtt
import json
import RPi.GPIO as GPIO, time
GPIO.setmode(GPIO.BCM)

Cloud_Host='XXXXXXXXXXX'
token = 'XXXXXXXXX'
sensor_data = {'LDR': 0}
client = mqtt.Client()
client.username_pw_set(token)
client.connect(Cloud_Host, 1883, 60)
client.loop_start()
try:
    def RCtime (PiPin):
        measurement = 0
        # Discharge capacitor
        GPIO.setup(PiPin, GPIO.OUT)
        GPIO.output(PiPin, GPIO.LOW)
        time.sleep(0.1)
        GPIO.setup(PiPin, GPIO.IN)
        # Count loops until voltage across
        # capacitor reads high on GPIO
        while (GPIO.input(PiPin) == GPIO.LOW):
            measurement += 1
        sensor_data['LDR'] = measurement
        client.publish('v1/devices/me/telemetry',json.dumps(sensor_data),1)
        return measurement

except KeyboardInterrupt:
    pass

while True:
    print RCtime(4) # Measure timing using GPIO4
    
    time.sleep(2)
client.loop_stop()
client.disconnect()
