import serial
import time
import struct 

serial_id = "usb-Arduino__www.arduino.cc__0043_75533343336351201241-if00"
path = "/dev/serial/by-id/"

ser = serial.Serial(path + serial_id, 9600, timeout=0)
on = str.encode('1')#1
init = str.encode('2')

ser.write(init)
time.sleep(0.1)

time.sleep(1)
ser.write(on)

