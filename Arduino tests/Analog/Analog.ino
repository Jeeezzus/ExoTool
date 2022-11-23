int A_0 = 0;
int A_2 = 0;
int A_3 = 0;
int A_1 = 0;

float ratio = 0.65;
void setup() {
   Serial.begin(115200);

}

void loop() {
  A_0 = (ratio * analogRead(A0)) + ((1-ratio) * A_0);
  A_1 = (ratio * analogRead(A1)) + ((1-ratio) * A_1);
  A_2 = (ratio * analogRead(A2)) + ((1-ratio) * A_2);
  A_3 = (ratio * analogRead(A3)) + ((1-ratio) * A_3);
  delay(110);
    Serial.println("A" + String(A_0) + "B" + String(A_1) + "C" + String(A_2) + "D" +String(A_3));

}
