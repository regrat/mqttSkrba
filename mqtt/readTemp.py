#!/usr/bin/python3
# temperature reader DS18B20 on RPI
# sudo raspi-config  (enable 1-wire)
# see https://electrosome.com/ds18b20-sensor-raspberry-pi-python/

import os
import glob
import time

os.system('modprobe w1-gpio')                        # load one wire communication device kernel modules

def read_temp_raw(device_file):
   f = open(device_file, 'r')
   lines = f.readlines()                             # read the device details
   f.close()
   return lines

def getSensors():
   path = "/sys/bus/w1/devices/28"
   sensors = []
   # Using '*' pattern
   for files in glob.glob(path + '*'):
      #print('Found:' + files)
      sensors.append(files + '/w1_slave')
   sensors.reverse()
   return(sensors)

#$ cat /sys/bus/w1/devices/28-0000044a0072/w1_slave 
#  40 01 4b 46 7f ff 10 10 1d : crc=1d YES
#4  0 01 4b 46 7f ff 10 10 1d t=20000
def read_temp1(sensor):
   lines = read_temp_raw(sensor)
   while type(lines) != list:
       if len(lines) != 2:
           continue
       x = lines[0].strip()
       if len(x) > 5 and x[-3:] != 'YES': # skip YES line
           continue
       else:
           time.sleep(0.2)
           lines = read_temp_raw(sensor)

   if len(lines) < 2:
       return ""
   equals_pos = lines[1].find('t=')                  # find temperature in the details
   #print("Read temp:" + lines[1])
   if equals_pos > 0:
      if len(lines[1]) > equals_pos + 2:
         temp_string = lines[1][equals_pos+2:]
         temp_c = float(temp_string) / 1000.0        # convert to Celsius
         return temp_c
   return ""

def read_temp():
   sensors = getSensors()
   out = []
   for sensor in sensors:
      out.append(read_temp1(sensor))
   return out

# read_temp()

