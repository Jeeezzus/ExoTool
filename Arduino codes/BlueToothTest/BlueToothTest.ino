#include <BluetoothSerial.h>

BluetoothSerial SerialBT;

void setup() {
  SerialBT.begin("ESP32test"); // Name of the ESP32 Bluetooth device
}

void loop() {
  SerialBT.println("Hello, world!");
  delay(1000);
}
