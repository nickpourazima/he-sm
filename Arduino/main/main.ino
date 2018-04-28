/* Author: Nick Pourazima
 * School: Carnegie Mellon University 
 * Department: Music Technology 
 * Contact: npourazima@gmail.com
 * Date: March 12, 2018
 */
 
//=================  PIN CONFIG =================

const byte buttonPin = 3; //Note: must be 3 for ProTrinket since only interrupt
const byte ledPin = 13;
//const byte ledPin2 = A4;
const uint8_t vibPins[] = {6,5,9,10};

//===============================================
//============== Button Thresholds ==============

const unsigned long max_threshold = 3000; // 3 second waiting period after last press before new bpm accepted
const unsigned long min_threshold = 300;  // 150 is sufficient but 300 is more certain for debounce

//===============================================
//============= Interrupt Variables =============
//
volatile unsigned long lastTriggered = 0;
volatile unsigned long newTime = 0;
volatile unsigned long sum = 0;
volatile unsigned long avg = 0;  //default 0 (test: 60 bpm = 1000 ms period)
volatile uint8_t count = 0;
volatile boolean start = false; //default false (set to true to start on boot) 

//===============================================
//========== State Machine Definitions ==========
#define READY 0
#define ON 1
#define OFF 2

uint8_t newState = READY;

#define START 0
#define RAMPUP_STEP_1 1
#define RAMPUP_STEP_2 2
#define RAMPUP_STEP_3 3
#define RAMPUP_STEP_4 4
#define RAMPDOWN_STEP_5 5
#define RAMPDOWN_STEP_6 6
#define RAMPDOWN_STEP_7 7
#define END 8

uint8_t state = START;
unsigned long startTime = 0;
int average = 0;

//boolean start = false;
//int avg = 0;

//===============================================
//============ Serial Trigger Setup =============

int incomingByte;   // for incoming serial data
boolean discrete = false; // flag for mode set (continous or discrete)

//===============================================

void setup() {
  Serial.begin(115200);
  // pinMode(ledPin, OUTPUT);
  pinMode(buttonPin,INPUT_PULLUP);
//  pinMode(ledPin2,OUTPUT);
  digitalWrite(buttonPin,HIGH);
  for(int i=0;i<4;i++){
    pinMode(vibPins[i],OUTPUT);
  }
  attachInterrupt(digitalPinToInterrupt(buttonPin), getAverage, FALLING); 
//  digitalWrite(ledPin2,LOW);
  // Serial.println("");
  // Serial.println("");
  // Serial.println("============   READY   ============");
  // Serial.println("Input desired operation mode, '1' (discrete/instantaneous)"); 
  // Serial.println("or '2' (continous/ramp up & down) and then press ENTER:");
  // Serial.println("-----------------------------------");
  // Serial.println("Next, input desired BPM and press ENTER:");
  // Serial.println("-----------------------");
  // Serial.println("To stop the motors, input '0'");
  // Serial.println("===================================");
}

void loop() {

//===============================================
// Uncomment below for LED indicator that tap is ready 
//===============================================
//  if((millis()-newTime)>max_threshold){
//    digitalWrite(ledPin2,HIGH);;
//  }
//  else{
//    digitalWrite(ledPin2,LOW);
//  }
  go();
  getBPM();
}

void getAverage() {
  unsigned long current = millis();
  unsigned long period = current - newTime;
//  start=false;
  if ((current-lastTriggered) < min_threshold) {
    lastTriggered = current;
    return;
  }
  lastTriggered = current;
  if (period > max_threshold) {
    count = 0;
    sum = 0;
  } else {
    sum += period;
    count++;
    avg = sum/count;
    start=true;
  }
  newTime = current;
}

void getBPM(){
  
  static char buffer[4];

  if(readline(Serial.read(),buffer,4)>0){
    incomingByte = atoi(buffer);
    if(incomingByte == 0){
      // Serial.println("=============   OFF   =============");
      start=false;
    }
    else if(incomingByte == 1){
      // Serial.println("---------- DISCRETE MODE ----------");
      discrete = true;         
    }
    else if(incomingByte == 2){
      // Serial.println("~~~~~~~~~~ CONTINOUS MODE ~~~~~~~~~");
      discrete = false;
    } 
    // else if(incomingByte < 20 || incomingByte > 220){
    //   Serial.println("Please input a BPM value greater than (or equal) to 20 and less than (or equal) to 220");
    // }
    else{
      avg = 60000/incomingByte;
      start = true;     
    }
  }
  
}

int readline(int readch, char *buffer, int len)
{
  static int pos = 0;
  int rpos;

  if (readch > 0) {
    switch (readch) {
      case '\n': // Ignore new-lines
        // Serial.write('\n');
//        break;
      case '\r': // Return on CR
        // Serial.write('\r');
        // Serial.write('\n');
        rpos = pos;
        pos = 0;  // Reset position index ready for next time
        return rpos;
      default:
        if (pos < len-1) {
          buffer[pos++] = readch;
          // Serial.write(readch);
          buffer[pos] = 0;
        }
    }
  }
  // No end of line has been found, so return -1.
  return -1;
}

void go(){
  if(discrete==true){
      switch (newState){
        case READY:
          if(start){
            average = avg;
            startTime=millis();
            Serial.println(startTime);
            newState++;
          }
          break;
        case ON: 
          digitalWrite(vibPins[0],HIGH);
          digitalWrite(vibPins[1],HIGH);
          digitalWrite(vibPins[2],HIGH);
          digitalWrite(vibPins[3],HIGH);
          // digitalWrite(ledPin,HIGH);
          if((millis()-startTime) >= ((average * 1)/4)){
            newState++;
          }
          break;
        case OFF:
          digitalWrite(vibPins[0],LOW);
          digitalWrite(vibPins[1],LOW);
          digitalWrite(vibPins[2],LOW);
          digitalWrite(vibPins[3],LOW);
          // digitalWrite(ledPin,LOW);
          if(millis()-startTime >= average){
            newState=0;
          }
          break;
        default:
          break;
      }
  }
  if(discrete==false){
      switch (state) {
        case START:
          if(start){
            average = avg;
            startTime=millis();
            Serial.println(startTime); 
            state++;
          }
          break;
        case RAMPUP_STEP_1:
          digitalWrite(vibPins[0],HIGH);
          // digitalWrite(ledPin,HIGH);
          if((millis()-startTime) >= ((average * 1)/7)){
            state++;
          }
          break;
        case RAMPUP_STEP_2:
          digitalWrite(vibPins[0],LOW);
          digitalWrite(vibPins[1],HIGH);
          if((millis()-startTime) >= ((average * 2)/7)){
            state++;
          }
          break;
        case RAMPUP_STEP_3:
          digitalWrite(vibPins[1],LOW);
          digitalWrite(vibPins[2],HIGH);
          if((millis()-startTime) >= ((average * 3)/7)){
            state++;
          }
          break;
        case RAMPUP_STEP_4:
          digitalWrite(vibPins[2],LOW);
          digitalWrite(vibPins[3],HIGH);
          if((millis()-startTime) >= ((average * 4)/7)){
            state++;
          }
          break;
        case RAMPDOWN_STEP_5:
          digitalWrite(vibPins[3],LOW);
          digitalWrite(vibPins[2],HIGH);
          if((millis()-startTime) >= ((average * 5)/7)){
            state++;
          }
          break;
        case RAMPDOWN_STEP_6:
          digitalWrite(vibPins[2],LOW);
          digitalWrite(vibPins[1],HIGH);
          if((millis()-startTime) >= ((average * 6)/7)){
            state++;
          }
          break;
        case RAMPDOWN_STEP_7:
          digitalWrite(vibPins[1],LOW);
          // digitalWrite(vibPins[0],HIGH);
          if((millis()-startTime) >= ((average * 7)/7)){
            state=0;
          }
          break;
        // case END:
        //   // digitalWrite(vibPins[0],LOW);
        //   // digitalWrite(ledPin,LOW);
        //   if((millis()-startTime) >= average){
        //     state=0; 
        //   }
          break;
        default:
          break;
      }
    }
}

