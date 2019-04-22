#include <AltSoftSerial.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
#define OLED_RESET     4 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
AltSoftSerial BTserial;

#define pin1 4

char myMessage[64];
int i; 
 
char c=' ';
boolean NL = true;
bool ne;
char printed[20];
int idx;
bool conn;
bool reading;
bool isSleep;
bool buttonstate;
bool curstate;
long int cur_time;
char F;

char sleep1[] = {'A','T','+','A','D','T','Y','3'};
char sleep2[] = {'A','T','+','S','L','E','E','P'};

char wake1[] = {'A','T','+','A','D','T','Y','0'};
char wake2[] = {'A','T','+','R','E','S','E','T'};
//char wake2[] = {'A','T','+','R','E','N','E','W'};

void setup()
{
    Serial.begin(9600);
    while(!Serial){};
    BTserial.begin(9600);  
    Serial.println("BTserial started");
    ne = false;
    conn = false;
    reading = false;
    isSleep = false;
    pinMode(pin1,INPUT_PULLUP);
    buttonstate = checkButton();
    curstate = buttonstate;

    //load display stuff
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3C for 128x32
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }

  // Show initial display buffer contents on the screen --
  // the library initializes this with an Adafruit splash screen.
  display.display();
  delay(2000); // Pause for 2 seconds

  // Clear the buffer
  display.clearDisplay();

  // Draw a single pixel in white
  display.drawPixel(10, 10, WHITE);

  // Show the display buffer on the screen. You MUST call display() after
  // drawing commands to make them visible on screen!
  display.display();
  delay(2000);
}

void loop()
{
    buttonstate = checkButton();
    if(buttonstate ^ curstate) {
      if (curstate) {
        isSleep = !isSleep;
        if (isSleep) {
          BTserial.write('A');
          BTserial.write('T');
          delay(500);
          for (int i = 0; i<8; i++) {
            BTserial.write(sleep1[i]);
          }
          while(BTserial.available()) {
            Serial.write(BTserial.read());
          }
          delay(500);
          for (int i = 0; i<8; i++) {
            BTserial.write(sleep2[i]);
          }
          while(BTserial.available()) {
            Serial.write(BTserial.read());
          }
          //Serial.flush();
          delay(500);
          conn = false;
        }
        else {
          F = BTserial.read();
          while(BTserial.read() != 'O') {
            BTserial.write('a');
            Serial.write(BTserial.read());
            delay(20);
          }
          while(BTserial.available()) {
            Serial.write(BTserial.read());
          }
          delay(500);
          for (int i = 0; i<8; i++) {
            BTserial.write(wake1[i]);
          }
          while(BTserial.available()) {
            Serial.write(BTserial.read());
          }
          delay(1000);
          for (int i = 0; i<8; i++) {
            BTserial.write(wake2[i]);
          }
          while(BTserial.available()) {
            Serial.write(BTserial.read());
          }
          delay(500);
        }
      }
    }
    curstate = buttonstate;
    // Read from the Bluetooth module and send to the Arduino Serial Monitor
    for (int i = 0; i < 20; i++) {
      printed[i] = '\0';
    }
    if (BTserial.available()) {
      reading = true;
    }
    while (reading)
    {
            c = BTserial.read();
            Serial.write(c);
            printed[idx] = c;
            idx++;
            delay(50);
            reading = BTserial.available();
    }
    
    // Read from the Serial Monitor and send to the Bluetooth module
    
    if (Serial.available())
    {
            c = Serial.read();
            
            
 
            // do not send line end characters to the HM-10
            if (c!=10 & c!=13 )
            {  
                 BTserial.write(c);
            }
 
            // Copy the user input to the main window, as well as the Bluetooth module
            // If there is a new line print the ">" character.
            if (NL) {
              Serial.print("\r\n>");
              NL = false;
            }
            Serial.write(c);
            if (c==10) {
              NL = true;
            }
    }

    if (idx > 0) {
      showMessage(printed);
    }
    idx = 0;
    if (printed[0] == 'C') {
      conn = true;
      cur_time = millis();
    }
    if (millis() - cur_time > 1000) {
      BTserial.write('*');
      cur_time = millis();
    }
    
}

void showMessage(char message[]) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0,0);
  display.cp437(true);
  int it = 0;

  while((message[it] != '\0') && (message[it] != '\n') && (it < 20)) {
    display.write(message[it]);
    it++;
  }
  display.display(); 
}

boolean checkButton() {
  bool ison;
  ison = digitalRead(pin1);
  return !ison;
}
