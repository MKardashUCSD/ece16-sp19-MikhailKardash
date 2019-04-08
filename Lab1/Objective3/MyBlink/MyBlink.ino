int counter; //counter variable
int del;
String inp;
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600); //begin serial
  counter = 0; //set counter to 0
  del = 1500; //default 1.5
}

void loop() {
  if (Serial.available() > 0) {
    inp = Serial.readStringUntil('\n'); //read a string until enter is hit
    if (inp == "SLOW") { //check for slow
        del = 1500;
      }
    else if (inp == "FAST") {  //check for fast
        del = 200;
    }
  }
  digitalWrite(LED_BUILTIN, HIGH);
  counter++; //increment counter
  Serial.print("Counter = "); //print counter to serial
  Serial.println(counter);   
  delay(del);     //1.5 sec delay                  
  digitalWrite(LED_BUILTIN, LOW);    
  delay(500);      //.5 sec delay                 
}
