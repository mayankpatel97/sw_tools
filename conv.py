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

if n < 3 : 
    print("Please enter the input and output filename.")
else:
    # Arguments passed
    print("\nInput File:", sys.argv[1])


        
    #file_path = "data/GNSS-RTK.txt"  # Replace with the actual file path
    #file_path = "data/KF_GINS_Navresult.nav"  # Replace with the actual file path
    file_path = sys.argv[1];
    #csv_path = "output.csv"  # Replace with the desired file path
    csv_path = sys.argv[2]  # Replace with the desired file path
    kml_file_name = "'points.kml'"
    delete_file_if_exists(kml_file_name)
    delete_file_if_exists(csv_path)
    kml=simplekml.Kml()
    csv_file = open(csv_path, 'w+')

    csv_file.write("col0,time,lat,lon,alt,x,y,z,p,q,r\n")
    limit = 0
    count =0
    try:
        file = open(file_path, 'r')
        file_contents = file.read()
        lines = file_contents.split('\n')
        #for line_number, line in enumerate(lines, start=1):
        for line_number in range(0,len(lines)-1):
            #print(f"Line {line_number}: {line}")
            input_string = lines[line_number]
            values = input_string.split()
            if values == None : break
            parsed_values = [float(value) for value in values]
            
    #        if len(values) > 4: 
                # Print the parsed values
            for index, value in enumerate(parsed_values, start=1):
                csv_file.write(f"{value},")
                


            #latitude = float(values[2])
            #longitude = float(values[3])

            
            # Convert to UTM
            #utm_easting, utm_northing = decimal_to_utm(latitude, longitude)
            #csv_file.write(str(utm_northing)+",")
            #csv_file.write(str(utm_easting))
            #print("UTM Easting:", utm_easting)
            #print("UTM Northing:", utm_northing)

            csv_file.write("\n")
            
            
            latitude = float(values[3])
            longitude = float(values[2])
            kml.newpoint(name="point" + str(count), coords=[(latitude,longitude)])
            count = count+1
            print("writing row : ",count)
            if limit > 0:
                limit -= 1
                if limit == 0: break
    except Exception as e:
        print("An error occurred:", e)
    
    csv_file.close()
    kml.save(kml_file_name)
    print("over")

