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
  # print(command)
  

# Open the serial port and when successful, execute the code that follows
with serial.Serial(port=serial_port, baudrate=9600, timeout=1) as ser:

    #NOTE 20 BYTE LIMIT ON COMMANDS
    # Set the name of the HM-10 module
    write_BLE("AT",ser)
    name = read_BLE(ser)
    print(name)
    # Print the response from the BLE module
    write_BLE("AT+IMME1",ser)
    name = read_BLE(ser)
    print(name)
    
    write_BLE("AT+NOTI1",ser)
    name = read_BLE(ser)
    print(name)
    
    write_BLE("AT+ROLE1",ser)
    name = read_BLE(ser)
    print(name)
    
    name = ""
    while not ("OK+CONNAOK+CONN" in name):
        write_BLE("AT+CONA810872197C7",ser)
        sleep(1)
        name = read_BLE(ser)
        print(name)
            
    
    #ser.reset_input_buffer
    #ser.reset_output_buffer
    write_BLE("Connected\n",ser)
    name = read_BLE(ser)
    print(name)
    
    num = 0;
    
    while(1):
        name = read_BLE(ser)
        sleep(.2)
        if '*' in name:
            num = num + 1
            write_BLE("Number: ",ser)
            write_BLE(str(num),ser)
            write_BLE('\n',ser)
            #b = read_BLE(ser)
    
    ser.close()
    # Ask for the name from the HM-10 module
    # Print the response from the BLE module