void setup() {
   Serial.begin(115200);

}

void loop() {
  delay(150);
    Serial.println("A" + String(analogRead(A0)) + "B" + String(analogRead(A1)) + "C" +String(analogRead(A2)) + "D" +String(analogRead(A3)));

}
