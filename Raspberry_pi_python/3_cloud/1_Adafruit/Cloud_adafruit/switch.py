import time
import RPi.GPIO as GPIO       ## Import GPIO library
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)      ## Use board pin numbering
GPIO.setup(17, GPIO.OUT)      ## Setup GPIO Pin 11 to OUT
 
# import Adafruit IO REST client.
from Adafruit_IO import Client, Feed, RequestError
 
# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = '6e5c062ba92f4393a13f949c2ba0c45f'
 
# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'sgravi2'
 
# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
 
try: # if we have a 'digital' feed
    digital = aio.feeds('switch')
except RequestError: # create a digital feed
    feed = Feed(name="switch")
    digital = aio.create_feed(feed)
 
while True:
    data = aio.receive(digital.key)
    print(data)
    if (data.value) == 'ON':
        GPIO.output(17,True)
        print('received <- ON\n')
    elif (data.value) == 'OFF':
        GPIO.output(17,False)
        print('received <- OFF\n')
    time.sleep(0.5)
