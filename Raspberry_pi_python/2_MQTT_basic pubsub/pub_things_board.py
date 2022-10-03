import paho.mqtt.client as paho
import time
import json
import random 

def on_connect(client, userdata, rc):
    print("Connection returned result: "+connack_string(rc))
 
def on_publish(client, userdata, mid):
    print("mid: "+str(mid))
    print("client: "+str(client))
    print("userdata: "+str(userdata))
    print ("Message Published...")
 
#ACCESS_TOKEN = 'D7P7kvsYZCfa2G67xIr1'
ACCESS_TOKEN='xta0ECffuswDYY6JXbnq'


 
client = paho.Client()
client.on_publish = on_publish
client.username_pw_set(ACCESS_TOKEN)
client.connect("demo.thingsboard.io", 1883)
client.loop_start()
attri={'temp':"",'Hum':''}
while True:    
    t=round(random.uniform(20,40),2)
    h=round(random.uniform(40,80),2)
    attri['ip']='www.google.com'
    attri['Hum']=h
    json.dumps(attri)
    (rc, mid) = client.publish("v1/devices/me/telemetry", json.dumps(attri), qos=1)
    print (rc)
    print (mid)
    time.sleep(5)
