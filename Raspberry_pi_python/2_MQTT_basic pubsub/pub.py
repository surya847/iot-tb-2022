import paho.mqtt.client as paho
import time
import json

def on_connect(client, userdata, rc):
    print("Connection returned result: "+connack_string(rc))
 
def on_publish(client, userdata, mid):
    print("mid: "+str(mid))
    print("client: "+str(client))
    print("userdata: "+str(userdata))
    print "Message Published..."

 
client = paho.Client()
client.on_publish = on_publish
client.connect("BROKER ADDRESS", 1883)
client.loop_start()
 
while True:
    attri={'temp':25}
    json.dumps(attri)
    (rc, mid) = client.publish("MQTTtopic", json.dumps(attri), qos=1)
    #print rc
    #print mid
    time.sleep(1)
