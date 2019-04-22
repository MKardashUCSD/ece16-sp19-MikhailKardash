"""
Send commands to the BLE module
"""

import serial
from time import sleep

serial_port = "COM9"                # You need to put the correct port


# Read from serial ser and return the string that was read
def read_BLE(ser):
  # Write your code here
  out = ''
  while (ser.in_waiting):
      out = out + ser.read(1).decode('utf-8')
  return out
  

# Write the string, command, to serial ser; return nothing
def write_BLE(command, ser):
  # Write your code here
  temp = command.encode('utf-8')
  work = ser.write(temp)
  sleep(.1)
  # print(command)
  

# Open the serial port and when successful, execute the code that follows
with serial.Serial(port=serial_port, baudrate=9600, timeout=1) as ser:

    #NOTE 20 BYTE LIMIT ON COMMANDS
    # Set the name of the HM-10 module
    write_BLE("AT+NAMEOOF",ser)
    name = read_BLE(ser)
    print(name)
    # Print the response from the BLE module
    write_BLE("AT+NAME?",ser)
    name = read_BLE(ser)
    print(name)
    
    ser.close()
    # Ask for the name from the HM-10 module
    # Print the response from the BLE module

    
    
    