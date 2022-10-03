#include <PubSubClient.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
/////////*    Network Configuration     */////////////

#define WIFI_SSID        "IoT"        //"TP-Link_CC93"          //WiFi SSID name
#define WIFI_PASSWORD    "kmvgrp96201"         //WiFi Pasword

///////*     Access  Token From CLOUD   *////////////

#define TOKEN "xta0ECffuswDYY6JXbnq"                    //access Token ID from the Server
char cloudServer[] = "demo.thingsboard.io";    //Cloud Server address

///////*     DHT11 setup    ////////////

#include "DHTesp.h"

#define DHTPIN 5
DHTesp dht;
#define switch 4
WiFiClient wifiClient;
PubSubClient client(wifiClient);

unsigned long lastSend;

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

void setup()
{
  Serial.begin(115200);                       // Initializing the Serial communication
  delay(10);
  InitWiFi();                                 // Setting up the network
  client.setServer( cloudServer, 1883 );      // Connecting with cloud Server
  lastSend = 0;
  pinMode(switch,OUTPUT);
  digitalWrite(switch,LOW );
  dht.setup(DHTPIN, DHTesp::DHT11);
}

// The callback for when a PUBLISH message is received from the server.
void on_message(const char* topic, byte* payload, unsigned int length) {

  Serial.println("On message");

  char json[length + 1];
  strncpy (json, (char*)payload, length);
  json[length] = '\0';

  Serial.print("Topic: ");
  Serial.println(topic);
  Serial.print("Message: ");
  Serial.println(json);

  // Decode JSON request
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& data = jsonBuffer.parseObject((char*)json);

  if (!data.success())
  {
    Serial.println("parseObject() failed");
    return;
  }
  String methodName = String((const char*)data["method"]);

   if (data["params"] == "ON"){
    digitalWrite(switch, HIGH);
   }
    if (data["params"] == "OFF"){
    digitalWrite(switch, LOW);
   }
}

void loop()
{
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
      client.subscribe("v1/devices/me/attributes");
    } else {
      Serial.print( "[FAILED] [ rc = " );
      Serial.print(client.state());
      Serial.println( " : retrying in 5 seconds]" );
      // Wait 5 seconds before retrying
      delay( 5000 );
    }
  }
}
