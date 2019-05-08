int sampleRate;
int reading;
float frequency;
long int prevTime;


void setup() {
  // put your setup code here, to run once:
  pinMode(A1,INPUT);
  sampleRate = 10;
  reading;
  frequency = (float) 1/sampleRate;
  prevTime = millis();
  Serial.begin(9600);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  if(millis() - prevTime > sampleRate) {
    prevTime = millis();
    reading = analogRead(A1);
    Serial.println(reading);
  }

}
