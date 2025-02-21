#include <ArduinoJson.h>  // Include the ArduinoJson library

void setup() {
  Serial.begin(115200);  // Initialize serial communication
  while (!Serial) {
    // Wait for the serial to be initialized
  }


}

void loop() {
  // Nothing to do in the loop for this example
  // Create a JSON document
  StaticJsonDocument<200> doc;
  doc["device"] = "ESP32";
  doc["status"] = "active";
  doc["temperature"] = 25.4;

  // Serialize JSON to string and send it over serial
  String output;
  serializeJson(doc, output);
  Serial.println(output);  // Send JSON string to serial port
  delay(5000);
}
