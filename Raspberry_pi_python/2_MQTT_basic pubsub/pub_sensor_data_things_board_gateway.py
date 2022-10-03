import paho.mqtt.client as paho
import time
import json
import Adafruit_DHT as dht
INTERVAL=2
def on_connect(client, userdata, rc):
    print("Connection returned result: "+connack_string(rc))
 
def on_publish(client, userdata, mid):
    print("mid: "+str(mid))
    print("client: "+str(client))
    print("userdata: "+str(userdata))
    print "Message Published..."

 
client = paho.Client()
client.on_publish = on_publish
client.connect("pi mqtt brokker ip", 1883)
client.loop_start()
 
while True:
    humidity,temperature = dht.read_retry(dht.DHT11, 4)
    if humidity is not None and temperature is not None:
        attri={"serialNumber": "SN-007", "sensorType": "Thermometer", "sensorModel": "T1000", "temp":temperature , "hum": humidity}
        json.dumps(attri)
        (rc, mid) = client.publish("/sensor/data", json.dumps(attri), qos=1)
        print(u"Temperature: {:g}*C, Humidity: {:g}%".format(temperature, humidity))        
    else:
        print( "Failed to get reading. Try again!")
    time.sleep(INTERVAL)
