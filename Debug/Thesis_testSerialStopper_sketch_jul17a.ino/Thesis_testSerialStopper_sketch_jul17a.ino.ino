int var = 0;
int currentVal = 0;
int ioPin = 4;

void setup() {
  Serial.begin(115200);
  pinMode(ioPin,INPUT);
}

void loop() {
  go();
}

void go(){
  currentVal = digitalRead(ioPin);
  if((var == 0) && (currentVal == 1))
  {
      Serial.println("onset");
  }
  var = currentVal;
}
