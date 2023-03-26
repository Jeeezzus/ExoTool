import serial

bluetooth = serial.Serial("/dev/rfcomm0", baudrate=9600)
while True:
    try:
        data = bluetooth.readline()
        print(data)
    except KeyboardInterrupt:
        bluetooth.close()
        break
