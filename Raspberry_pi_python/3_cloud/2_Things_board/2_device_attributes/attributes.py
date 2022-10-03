import os
import time
import sys
import paho.mqtt.client as mqtt
import json
import RPi.GPIO as GPIO
import socket
import struct
import fcntl


Cloud_HOST = 'XXXXXXXXXXX'
ACCESS_TOKEN = 'xxxxxxxxxx'

client = mqtt.Client()
# Register connect callback
attri = {'System Status' : '\0', 'MAC': '\0', 'IP adress': '\0', 'Temperature':'\0'}
inter = 0
attri['System Status'] = 'Online'
client.publish('v1/devices/me/attributes', json.dumps(attri), 1)

client.username_pw_set(ACCESS_TOKEN)
# Connect to Cloud using default MQTT port and 60 seconds keepalive interval
client.connect(Cloud_HOST, 1883,60)

def on_connect(client, userdata,flags, rc):
    print 'Connected to Cloud'
    client.subscribe('v1/devices/me/attributes')
    
def on_message(client, userdata, msg):
    print 'Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload)
    global inter
    data = json.loads(msg.payload)

    inter = data['command']
    print inter
    os.system(inter)
    
    if data['command']=="ifconfig":
        os.system(inter)
        s= get_interface_ipaddress('wlan0')
        attri['IP adress'] = s
        print s
        client.publish('v1/devices/me/attributes', json.dumps(attri), 1)
    if data['command']=="mac":
        os.system(inter)
        myMAC = open('/sys/class/net/eth0/address').read()
        attri['MAC'] = myMAC
        print myMAC
        client.publish('v1/devices/me/attributes', json.dumps(attri), 1)
    if data['command']=="reboot":
        attri['System Status'] = inter
        client.publish('v1/devices/me/attributes', json.dumps(attri), 1)
        time.sleep(3)
        os.system(inter)
    if data['command']=="temp":
        temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
        print temp
        attri['Temperature'] = temp
        client.publish('v1/devices/me/attributes', json.dumps(attri), 1)  
    if data['command']=="shutdown":
        attri['System Status'] = inter
        client.publish('v1/devices/me/attributes', json.dumps(attri), 1)
        os.system(inter)
    
def get_interface_ipaddress(network):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', network[:15])  
        )[20:24])

def main():
    client.on_connect = on_connect
    # Registed publish message callback
    client.on_message = on_message

main()

try:
    client.loop_forever()
except KeyboardInterrupt:
    GPIO.cleanup()
