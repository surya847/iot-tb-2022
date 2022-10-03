import time
 
# import adafruit dht library.
import Adafruit_DHT
 
# import Adafruit IO REST client.
from Adafruit_IO import Client, Feed, RequestError
 
# Delay in-between sensor readings, in seconds.
DHT_READ_TIMEOUT = 4
 
# Pin connected to DHT22 data pin
DHT_DATA_PIN = 4
 
# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = '6e5c062ba92f4393a13f949c2ba0c45f'
 
# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username).
ADAFRUIT_IO_USERNAME = 'sgravi2'
 
# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
 
# Set up Adafruit IO Feeds.
temperature_feed = Feed(name='temperature')
humidity_feed = Feed(name='humidity')


try:
    feed1=aio.feeds('temperature')
    feed2=aio.feeds('humidity')
except RequestError:
    feed1=aio.create_feed(humidity_feed)
    feed2=aio.create_feed(temperature_feed)
# Set up DHT11 Sensor.
dht11_sensor = Adafruit_DHT.DHT11
 
while True:
    humidity, temperature = Adafruit_DHT.read_retry(dht11_sensor, DHT_DATA_PIN)
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
        # Send humidity and temperature feeds to Adafruit IO
        temperature = '%.2f'%(temperature)
        humidity = '%.2f'%(humidity)
        aio.send(feed2.key, str(temperature))
        aio.send(feed1.key, str(humidity))
    else:
        print('Failed to get DHT11 Reading, trying again in ', DHT_READ_TIMEOUT, 'seconds')
    # Timeout to avoid flooding Adafruit IO
    time.sleep(DHT_READ_TIMEOUT)
