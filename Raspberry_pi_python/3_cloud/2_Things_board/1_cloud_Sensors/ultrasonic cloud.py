import RPi.GPIO as GPIO
import time
import sys
import paho.mqtt.client as mqtt
import json

Cloud='XXXXXXXXXXX'
token = 'XXXXXXXXXXXX'
sensor_data = {'Distance': 0}

client = mqtt.Client()

# Set access token
client.username_pw_set(token)

client.connect(Cloud, 1883, 60)

client.loop_start()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TRIG = 23 
ECHO = 24
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

try:
    while True:
        GPIO.output(TRIG, False)
        print "Waiting For Sensor To Settle"
        time.sleep(2)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO)==0:
          pulse_start = time.time()

        while GPIO.input(ECHO)==1:
          pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150

        distance = round(distance, 2)

        print "Distance:",distance,"cm"
        sensor_data['Distance'] = distance
        client.publish('v1/devices/me/telemetry',json.dumps(sensor_data),1)

except KeyboardInterrupt:
    pass
GPIO.cleanup()
client.loop_stop()
client.disconnect()
