#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
#define OLED_RESET     4 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#define NUMFLAKES     10 // Number of snowflakes in the animation example

#define LOGO_HEIGHT   16
#define LOGO_WIDTH    16
static const unsigned char PROGMEM logo_bmp[] =
{ B00000000, B11000000,
  B00000001, B11000000,
  B00000001, B11000000,
  B00000011, B11100000,
  B11110011, B11100000,
  B11111110, B11111000,
  B01111110, B11111111,
  B00110011, B10011111,
  B00011111, B11111100,
  B00001101, B01110000,
  B00011011, B10100000,
  B00111111, B11100000,
  B00111111, B11110000,
  B01111100, B11110000,
  B01110000, B01110000,
  B00000000, B00110000 };
    char myMessage[64];
  int i;

//MYCODE_START
bool toggle;
bool buttonstate;
bool curstate;
long int timRef;
int seconds;
int pin1 = 4;
char beginStr[] = {'B','e','g','i','n','\0'};
char endStr[22] = {'E','n','d',' ','T','i','m','e',':',' '};
char secondsC[4] = {'\0','\0','\0','\0'};
char milli[3];
int L;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(pin1, INPUT_PULLUP);
  toggle = 0;
  timRef = 0;
  seconds = 0;
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

void loop() {
  // put your main code here, to run repeatedly:
  curstate = checkButton();
  if (buttonstate ^ curstate) {  //faster to xor
    if (curstate) { //if switching from 0 to 1, toggle.
      toggle = !toggle; //invert.
      if (toggle) { //begin timer.
        showMessage(beginStr);
      }
      else  {
        itoa(millis() - timRef,milli,10);
        itoa(seconds,secondsC,10);        
        L = 0;
        while((secondsC[L] != '\0') & (L < 4)) {
          endStr[10+L] = secondsC[L];
          L++;
        }
        L = 10+L;
        endStr[L] = '.';
        L++;
        for (int k = 0; k <=2; k++) {
          endStr[L+k] = milli[k];        
        }
        endStr[L+3] = 's';
        endStr[L+4] = '\0';
        showMessage(endStr);
        for (int k = 10; k <= 21; k++) {
          endStr[k] = '\0';
        }
        for (int k = 0; k <= 3; k++) {
          secondsC[k] = '\0';
        }
      }
      timRef = millis();
    }
  }
  if (toggle) {  //second counter
    if (millis() - timRef >= 1000) {
      seconds++;
      timRef = timRef + 1000;
      //Serial.println(seconds);
      showNum(seconds);
    }
  }
  else {
    seconds = 0;
  }
  buttonstate = curstate;
}

boolean checkButton() {
  bool ison;
  ison = digitalRead(pin1);
  return !ison;
}

void showNum(int k) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0,0);
  display.cp437(true);

  char tempN[4];
  
  itoa(k,tempN,10);

  int it = 0;

  while((tempN[it] != '\0') && (tempN[it] != '\n') && (it < 4)) {
    display.write(tempN[it]);
    it++;
  }  
  display.display();
}

void showMessage(char message[]) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0,0);
  display.cp437(true);
  int it = 0;

  while((message[it] != '\0') && (message[it] != '\n')) {
    display.write(message[it]);
    it++;
  }
  display.display(); 
}

