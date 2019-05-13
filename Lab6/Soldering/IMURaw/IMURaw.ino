/* 
 *  General Includes
 */
#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include "Wire.h"

/* 
 *  Global Variables
 */
const int MPU_addr=0x68;  // I2C address of the MPU-6050
MPU6050 IMU(MPU_addr);
const int interruptPin = 2;
volatile bool ipinReady = false;
int16_t ax, ay, az, tp, gx, gy, gz;

unsigned long startTime = 0;
unsigned long endTime = 0;
unsigned long volatile elapsedTime = 0;
unsigned long period_us = 50000; // 20Hz

/* 
 *  Function to check the interrupt pin to see if there is data available in the MPU's buffer
 */
void interruptPinISR() {
  ipinReady = true;
}

/* 
 *  Function to read a single sample of IMU data
 *  NOTE: IN YOUR FINAL PROJECT/PROGRAMS, ONLY READ WHAT YOU INTEND TO USE IN YOUR ALGORITHM!
 */
void readIMU() {
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B);                    // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  
  Wire.requestFrom(MPU_addr,14,true);  // request a total of 14 registers
  
  //Accelerometer (3 Axis)
  ax=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)    
  ay=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  az=Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  
  //Temperature
  tp=Wire.read()<<8|Wire.read();  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
  
  //Gyroscope (3 Axis)
  gx=Wire.read()<<8|Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  gy=Wire.read()<<8|Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  gz=Wire.read()<<8|Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
}

/* 
 * Function to grab new samples at 20Hz
 */
bool grabSamples()
{
  bool newSamples = false;
  if (ipinReady)
  {
    endTime = micros();
    elapsedTime = endTime - startTime;
    if (elapsedTime >= period_us) 
    {
      readIMU();                    // read data from the IMU
      startTime = endTime;          // “reset” the timer
      newSamples = true;
    }
  }
  return newSamples;
}

/* 
 *  Function to send data to the Python processing
 *  NOTE: MODIFY ACCORDING TO YOUR ALGORITHM!
 */
void sendData() {
//  Serial.print(elapsedTime);          // Uncomment these lines to print timestamps
//  Serial.print(' ');                  // Uncomment these lines to print timestamps
  Serial.print(ax);
  Serial.print(' ');
  Serial.print(ay);
  Serial.print(' ');
  Serial.print(az);
  Serial.print(' ');
  Serial.print(gx);
  Serial.print(' ');
  Serial.print(gy);
  Serial.print(' ');
  Serial.print(gz);
  Serial.println(',');
}

/* 
 *  Function to do the usual Arduino setup
 */
void setup(){

  // Intialize the IMU and the DMP (Digital Motion Processor) on the IMU
  IMU.initialize();
  IMU.dmpInitialize();
  IMU.setDMPEnabled(true);

  // Initialize I2C communications
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(MPU_addr);   // PWR_MGMT_1 register
  Wire.write(0);          // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);

  // Initialize Serial port
  Serial.begin(9600);

  // Create an interrupt for pin2, which is connected to the INT pin of the MPU6050
  pinMode(interruptPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(interruptPin), interruptPinISR, RISING);

  // Start time of the Arduino (for elapsed time)
  startTime = micros();
}

/* 
 *  Function to loop continuously: poll ==> send ==> read
 *  NOTE: MODIFY TO SUIT YOUR ALGORITHM!
 */
void loop(){
  
  if(grabSamples())
    sendData();
}