import serial
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
while True:
     print(ser.readline().strip())