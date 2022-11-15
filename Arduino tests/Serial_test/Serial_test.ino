int targetValues[4];
int actualValues[4];
float incrValues[4];
#define time_to_target 10
void setup() {
  Serial.begin(115200);
  for (int i = 0; i<4; i++){
    actualValues[i] = 0;
  }
}

void loop() {

  for (int i = 0; i<4; i++){
    targetValues[i] = random(0, 1023);
  }

  for (int i = 0; i<4; i++){
    incrValues[i] = (targetValues[i] - actualValues[i])/time_to_target;
  }
  for (int i = 0; i<time_to_target; i++){
     delay(150);
    Serial.println("A" + String(int(actualValues[0] + (incrValues[0] * i))) + "B" + String(int(actualValues[1] + (incrValues[1] * i))) + "C" + String(int(actualValues[2] + (incrValues[2] * i))) + "D" + String(int(actualValues[3] + (incrValues[3] * i))) + "");
  }
  for (int i = 0; i<4; i++){
    actualValues[i] = targetValues[i];
  }
}
