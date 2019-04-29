"""
Example of live plotting
"""

# Import custom libraries
from Libraries.ListBuffer import ListBuffer
from Libraries.AnimatedFigure import AnimatedFigure

# Import time library
import time as tm
# This is only needed for our example data we are using
# You can delete this when you are using your actual sensor data
import numpy as np              # Numpy library
current_time = tm.clock()                # Current time
start_time = tm.clock()                  # Start time
sampling_freq = 50              # [Hz]
sampling_period = 1 / sampling_freq     # [s]

# create var

global write_flag 
write_flag = False
global write_path 
write_path = "data_write.csv"
global read_flag
read_flag = not write_flag

global filename
global openarg
    


def opentype(write_flag,read_flag):
    if (write_flag):
        val = "w"
        print("WWW")
    elif(read_flag):
        val = "r"
        print("RRR")
    else:
        print("defaulting to read")
        val = "r"
    return val

openarg = opentype(write_flag,read_flag)
filename = open(write_path,openarg)

# Should we plot our data or not
live_plot = True


from Libraries.Bt_basic_handshake import Bt


# Set peripheral MAC as well as HM-10 serial port
ble_peripheral_MAC = "A810872197C7"                 # Use the MAC address of your peripheral HM-10
serial_port = 'COM9'


    
# Initialization of BLE
def initialize_ble():
    global bt
    bt = Bt(ble_peripheral_MAC=ble_peripheral_MAC, serial_port=serial_port)
    bt.ble_setup()


# Initialize buffers
def initialize_buffers():
    
    # Set shared variables to global so we can modify them
    global data_buffer

    # Create empty buffers to store data
    buffer_length = 50 * 30         # Initial estimate for 30 sec of data at 50Hz, that's probably way too long!
    data_buffer = [[]] * 2          # Two sets of data: time and sensor data
    data_buffer[0] = ListBuffer([], maxlen=buffer_length)       # time data
    data_buffer[1] = ListBuffer([], maxlen=buffer_length)       # sensor data


# This is just an example function
# You will want to replace this with the proper function to get data, e.g., from BLE 
def get_data():
    global current_time
    global start_time
    if (openarg == 'r'):
        while True:
            if (tm.clock() - start_time > sampling_period):
                start_time = tm.clock()
                response = filename.readline()
                break
    elif (openarg == 'w'):
        while True:
            response = bt.ble_read_line(eol = ';')
            if response:
                filename.write(response)
                filename.write('\n')
                break
    temp = response.split(",")
    data = [float(temp[0]),int(temp[1])]
    return data

    
# The main data processing function
# It is called repeatedly
def update_data():
    global data_buffer

    data = None
    while not data:                                 # Keep looping until valid data is captured
        data = get_data()                                                 

    # Add this new data to circular data buffers
    data_buffer[0].add(data[0])                   # time data
    data_buffer[1].add(data[1])                   # sensor data

    return [(data_buffer[0], data_buffer[1])]
    # This format [(x1, y1), (x2, y2), (x3, y3)] is expected by the animation module


"""
This is where the main code starts
"""
try:
    # Take care of some initializations
    initialize_buffers()
    # Take care of some initializations
    if not (read_flag):
        initialize_ble()
    
    # If we are plotting our data
    # Call the animation with our update_data() function
    # This will call our function repeatedly and plot the results
    if live_plot:
        # Create animation object
        # Plot about 1/5 of the data in the buffer
        an = AnimatedFigure(update_data, plot_samples=200, debug=True)
        axes = an.axes
        axes[0].set_title('Data')
        axes[0].set_xlabel('Time (s)')
        axes[0].set_ylabel('Position (units?)')

        an.animate()            # Only call this after configuring your figure

    # If we don't want to plot at the same time, call the update_data() function repeatedly
    else:
        while True:
            update_data()
            
# Catch the user pressing Ctlr+C            
except (Exception, KeyboardInterrupt) as e:
    filename.close()
    print(e)