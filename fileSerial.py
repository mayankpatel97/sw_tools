#!/usr/bin/env
import sys
import matplotlib.pyplot as plt
import numpy as np
import math



from pyproj import Proj
import numpy as np


import pyproj
import os

import csv
import simplekml
import serial
from datetime import datetime


def decimal_to_utm(latitude, longitude):
    # Define the input and output coordinate systems
    wgs84 = pyproj.CRS("EPSG:4326")  # WGS84 geographic coordinate system (decimal degrees)
    #zone = "44" # 44R utm zone , noida
    zone = "50" # china
    utm = pyproj.CRS("EPSG:326" + zone)    # UTM Zone 32N for example (replace with your desired UTM zone)

    # Create a Proj object for the conversion
    transformer = pyproj.Transformer.from_crs(wgs84, utm, always_xy=True)

    # Perform the conversion
    utm_easting, utm_northing = transformer.transform(longitude, latitude)

    return utm_easting, utm_northing




def delete_file_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File '{file_path}' deleted.")
    else:
        print(f"File '{file_path}' does not exist.")

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    print("scaning serial com ports")
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
'''
# Example coordinates (decimal degrees)
latitude = 28.0
longitude = 79.0

# Convert to UTM
utm_easting, utm_northing = decimal_to_utm(latitude, longitude)

print("UTM Easting:", utm_easting)
print("UTM Northing:", utm_northing)

'''

n = len(sys.argv)
#print("Total arguments passed:", n)

if sys.argv[1] == "-listcom":
    print(serial_ports())

if n < 3 : 
    print("Please enter the file name and port.")
    print("Example : write_serial.py file.txt COM5.")
else:
    # Arguments passed
    print("\nInput File:", sys.argv[1])


        
    #file_path = "data/GNSS-RTK.txt"  # Replace with the actual file path
    #file_path = "data/KF_GINS_Navresult.nav"  # Replace with the actual file path
    input_file_path = sys.argv[1]
    com_port = sys.argv[2]
    #csv_path = "output.csv"  # Replace with the desired file path
    #csv_path = sys.argv[2]  # Replace with the desired file path

    print("File : ", input_file_path)
    print("Serial COM : ", com_port)
    prev_millis=0
    try:
        infile = open(input_file_path, 'r+')
        ser = serial.Serial(com_port, baudrate=230400, timeout = 1)
        while True: 
            #print("Current date:",datetime.utcnow())
            date= datetime.utcnow() - datetime(1970, 1, 1)
            #print("Number of days since epoch:",date)
            seconds =(date.total_seconds())
            milliseconds = round(seconds*1000)
            #print("Milliseconds since epoch:",milliseconds)
            if milliseconds - prev_millis < 5 : continue
            prev_millis = milliseconds

            line = infile.readline()
            if line != '':
                print(str(milliseconds) + ":" + line)
                ser.write(line.encode("utf-8"))
            else:   break
        
        infile.close()
        ser.close()
        print("over")

    except KeyboardInterrupt:
        infile.close()
        ser.close()
        print("stopped!")
    except Exception as e:
        print("An error occurred:", e)
    


