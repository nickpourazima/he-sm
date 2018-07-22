void setup() {
  Serial.begin(115200);
  pinMode(8,OUTPUT);
  pinMode(13,OUTPUT);
}

void loop() {
  go();
}

void go(){
  digitalWrite(8,HIGH);
  digitalWrite(13,HIGH);
  Serial.println("onset");
  delay(500);
  digitalWrite(8,LOW);
  digitalWrite(13,LOW);
  delay(500);
}
