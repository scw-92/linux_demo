# -*- coding: utf-8 -*-
import serial
import os
from time import sleep
if __name__ == '__main__':
    serial = serial.Serial('/dev/ttyUSB0', 9600,timeout = 3600)
    if serial.isOpen() :
        print("open success")
    else :
        print("open failed")
    while True:
        #send_data = input("input a data: ")
        #send_data = send_data + '\r\n'
        #serial.write(send_data.encode())
        data=serial.read(1)
        if data:
            sleep(0.1)
            n = serial.inWaiting()
            if n:
                data = data + ser.read(n)
                print(data.decode())
        data = ''
        #sleep(0.1)
        #data = (data + serial.read(serial.inWaiting())).decode()
        #:print(data)

