/* Author: Nick Pourazima
 * School: Carnegie Mellon University 
 * Department: Music Technology 
 * Contact: npourazima@gmail.com
 * Date: July 14, 2018
 * Note: This rev is based on the Bluz board running particle I/O and as such has been modified from the original main.ino
 */

//=================  PIN CONFIG =================
const byte ledPin = D7;
const uint8_t vibPins[] = {D0,D1,D2,D3};

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
unsigned long avg = 0;
boolean start = false;

//===============================================
//============ Serial Trigger Setup =============

int incomingByte;   // for incoming serial data
boolean discrete = false; // flag for mode set (continous or discrete)

//===============================================

void setup() {
    pinMode(ledPin,OUTPUT); 
    for(int i=0;i<4;i++){
        pinMode(vibPins[i],OUTPUT);
        digitalWrite(vibPins[i],LOW);
    }
    Particle.function("motor",motorToggle);
}

void loop() {
    // System.sleep(SLEEP_MODE_CPU); //battery saver but throws off accuracy of timing intervals
    SINGLE_THREADED_BLOCK(){
        go();
    }
}

int motorToggle(String command) {
    if(command == "off" or command == "0"){
        start=false;
        return 0;
    }
    else if(command == "1"){
        discrete = true;  
        return 1;
    }
    else if(command == "2"){
        discrete = false;
        return 2;
    } 
    else{
        avg = 60000/atoi(command);
        start = true;   
        return avg;
    }
}

void go(){
    if(discrete==true){
        switch (newState){
            case READY:
                if(start){
                    average = avg;
                    startTime=millis();
                    newState++;
                }
                break;
            case ON:
                digitalWrite(vibPins[0],HIGH);
                digitalWrite(vibPins[1],HIGH);
                digitalWrite(vibPins[2],HIGH);
                digitalWrite(vibPins[3],HIGH);
                digitalWrite(ledPin,HIGH);
                if((millis()-startTime) >= ((average * 1)/4)){
                    newState++;
                    // Serial.println("onset");
                }
                break;
            case OFF:
                digitalWrite(vibPins[0],LOW);
                digitalWrite(vibPins[1],LOW);
                digitalWrite(vibPins[2],LOW);
                digitalWrite(vibPins[3],LOW);
                digitalWrite(ledPin,LOW);
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
                    state++;
                }
                break;
            case RAMPUP_STEP_1:
                digitalWrite(vibPins[0],HIGH);
                digitalWrite(ledPin,HIGH);
                if((millis()-startTime) >= ((average * 1)/9)){
                    state++;
                }
                break;
            case RAMPUP_STEP_2:
                digitalWrite(vibPins[0],LOW);
                digitalWrite(vibPins[1],HIGH);
                if((millis()-startTime) >= ((average * 2)/9)){
                    state++;
                }
                break;
            case RAMPUP_STEP_3:
                digitalWrite(vibPins[1],LOW);
                digitalWrite(vibPins[2],HIGH);
                if((millis()-startTime) >= ((average * 3)/9)){
                    state++;
                    // Serial.println("onset");
                }
                break;
            case RAMPUP_STEP_4:
                digitalWrite(vibPins[2],LOW);
                digitalWrite(vibPins[3],HIGH);
                if((millis()-startTime) >= ((average * 5)/9)){
                    state++;
                }
                break;
            case RAMPDOWN_STEP_5:
                digitalWrite(vibPins[3],LOW);
                digitalWrite(vibPins[2],HIGH);
                if((millis()-startTime) >= ((average * 6)/9)){
                    state++;
                }
                break;
            case RAMPDOWN_STEP_6:
                digitalWrite(vibPins[2],LOW);
                digitalWrite(vibPins[1],HIGH);
                if((millis()-startTime) >= ((average * 7)/9)){
                    state++;
                }
                break;
            case RAMPDOWN_STEP_7:
                digitalWrite(vibPins[1],LOW);
                digitalWrite(vibPins[0],HIGH);
                if((millis()-startTime) >= ((average * 8)/9)){
                    state++;
                }
                break;
            case END:
                digitalWrite(vibPins[0],LOW);
                digitalWrite(ledPin,LOW);
                if((millis()-startTime) >= average){
                    state=0; 
                }
                break;
            default:
                break;
        }
    }
}