import serial
import time
import serial.tools.list_ports


def portsDetection():
     print("waiting for connection...")
     ports = list(serial.tools.list_ports.comports())
     for p in ports:
          print(p.manufacturer)
          if "Arduino" in p.manufacturer:
               print("This is an Arduino!")
               return(serial.Serial(str(p.device), 115200, timeout=10))
     raise Exception("No device Found")

found = False
ser = "none"
while found == False:
     time.sleep(1)
     try:
          ser = portsDetection()
          found = True
     except Exception:
          found = False
          

alpha = [0,0,0,0]
errcpt = 0
while True:
     try:
          strval = ser.readline().decode().strip()
          print(strval)
          if "A" in strval:
               alpha[0] = ((int(strval.split("A")[1].split("B")[0])*1.8)/1024)-0.8
               alpha[1] = ((int(strval.split("B")[1].split("C")[0])*1.8)/1024)-0.8
               alpha[2] = ((int(strval.split("C")[1].split("D")[0])*1.8)/1024)-0.8
               alpha[3] = ((int(strval.split("D")[1])*1.8)/1024)-0.8
               print(alpha)
               errcpt = 0
     except Exception:
          errcpt += 1
          if (errcpt >= 5):
               print("Connection error, please check cables")
               found = False
               while found == False:
                    time.sleep(1)
                    try:
                         ser = portsDetection()
                         found = True
                    except Exception:
                         found = False
          pass