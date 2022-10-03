#include <PubSubClient.h>
#include <ESP8266WiFi.h>

/////////*    Network Configuration     */////////////

#define WIFI_SSID      "XXXXXXXXXXX"          //WiFi SSID name
#define WIFI_PASSWORD  "XXXXXXXXXXX"         //WiFi Pasword

///////*     Access  Token From CLOUD   *////////////

#define TOKEN "XXXXXXXXXXXXXXXXX"                    //access Token ID from the Server
char cloudServer[] = "demo.thingsboard.io";    //Cloud Server address

///////*     DHT11 setup    ////////////
#include "DHTesp.h"
#define DHTPIN 5
DHTesp dht;

WiFiClient wifiClient;
PubSubClient client(wifiClient);

unsigned long lastSend;

void setup()
{
  Serial.begin(115200);                       // Initializing the Serial communication
  delay(10);
  InitWiFi();                                 // Setting up the network
  client.setServer( cloudServer, 1883 );      // Connecting with cloud Server
  dht.setup(DHTPIN, DHTesp::DHT11);
  lastSend = 0;
   if ( !client.connected() )
  {
    reconnect();
  }

  if ( millis() - lastSend > 1000 )
  {
    temperature_humidity();                      //Function call
    lastSend = millis();
  }

  client.loop();
   Serial.println("Going into deep sleep for 20 seconds");
  ESP.deepSleep(20e6); // 20e6 is 20 microseconds
}

void loop()
{
 
}


void temperature_humidity()                           //Function to collect the Temperature and Humidity
{
  Serial.println("Collecting temperature data.");
  delay(dht.getMinimumSamplingPeriod());
  float h = dht.getHumidity();                       // Reading humidity
  float t = dht.getTemperature();                    // Read temperature as Celsius
  String temperature = String(t);
  String humidity = String(h);
  
  String payload = "{";
  payload += "\"temperature\":";
  payload += temperature;
  payload += ",";
  payload += "\"humidity\":";
  payload += humidity; 
  payload += "}";   

  char attributes[100];
  payload.toCharArray( attributes, 100 );
  client.publish( "v1/devices/me/telemetry", attributes );
  Serial.println( attributes );

}
void InitWiFi()                                       //Setup to connect through WiFi network
{
  Serial.println("Connecting to AP ...");

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to AP");
}


void reconnect()                                      //Reconnecting with MQTT
{
  while (!client.connected())
  {

    if (  WiFi.status() != WL_CONNECTED)
    {
      WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
      while (WiFi.status() != WL_CONNECTED)
      {
        delay(500);
        Serial.print(".");
      }
      Serial.println("Connected to AP");
    }
    Serial.print("Connecting to CLOUD ...");
    // Attempt to connect (clientId, username, password)
    if ( client.connect("ESP8266 Device", TOKEN, NULL) ) {
      Serial.println( "[DONE]" );
    } else {
      Serial.print( "[FAILED] [ rc = " );
      Serial.print(client.state());
      Serial.println( " : retrying in 5 seconds]" );
      // Wait 5 seconds before retrying
      delay( 5000 );
    }
  }
}
