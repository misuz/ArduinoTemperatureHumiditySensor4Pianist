#include <WiFi.h>
#include <Ambient.h>
#include <DHT.h>

#define channelId {YOUR_CHANNEL_ID}     // Ambient channel ID
#define writeKey "{YOUR_CHANNEL_KEY}"   // Ambient write key
#define DHTPIN 13                       // GPIO pin number
#define DHTTYPE DHT11                   // Change to DHT12 if using a DHT12 sensor
#define SERIAL_BAUD_RATE 115200         // Baud rate for serial communication
#define SEND_INTERVAL 60000             // Measurement interval (milliseconds)
const char *ssid = "{YOUR_WIFI_SSID}";          // Wi-Fi SSID
const char *password = "{YOUR_WIFI_PASSWORD}";  // Wi-Fi password


WiFiClient client;
Ambient ambient;
DHT dht(DHTPIN, DHTTYPE);


void setup() {
  Serial.begin(SERIAL_BAUD_RATE);
  delay(2000);

  // Connect to Wi-Fi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("[INFO] Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n[INFO] WiFi Successfully Connected!");

  // Initialize Ambient
  ambient.begin(channelId, writeKey, &client);

  // Initialize DHT
  dht.begin();
}

void loop() {

  // Read temperature and humidity from DHT11
  float t = dht.readTemperature(); // Temperature
  float h = dht.readHumidity();    // Humidity

  if (isnan(t) || isnan(h)) {
    // Measurement failed
    Serial.println("[ERROR] Measurement failed!");
    delay(2000);
    return;
  }

  // Measurement successful
  Serial.println("[INFO] Temperature: " + String(t, 1) + "C   Humidity: " + String(h, 1) + "%");

  // Send data to Ambient
  ambient.set(1, t);
  ambient.set(2, h);

  if (ambient.send()) {
    // Send succeeded
    Serial.println("[INFO] Ambient Send Success!");
  } else {
    // Send failed
    Serial.println("[ERROR] Ambient Send Failed!");
  }

  delay(SEND_INTERVAL); // Send once per minute
}
