# -*- coding: utf-8 -*-
import serial
import os
from time import sleep

# 传感器地址  
#   文档、空气湿度   ： 01
#   土壤              ： 02
# 光照强度               03
# co2                   04


class Crc():
    def __init__(self):
        self.crc_result = 0xffff

    def ca_crc(self, data_array):
        self.crc_result = 0xffff
        #for index in range(len(data_array) - 2):
        for index in range(len(data_array)):
            #print("0x%x" % data_array[index])

            self.crc_result ^= data_array[index]
            crc_num = (self.crc_result & 0x0001)

            for m in range(8):
                if crc_num :
                    xor_flag = 1;
                else:
                    xor_flag = 0

                self.crc_result >>= 1;

                if (xor_flag):
                    self.crc_result ^= 0xa001

                crc_num = (self.crc_result & 0x0001)
        
        return [ self.crc_result & 0xff, self.crc_result >> 8 ]


if __name__ == '__main__':
    #ser = serial.Serial('/dev/ttyO1', 115200,timeout = 1)
    
    crcc = Crc()
    
    
    
    
    
    
    
    crc_data10 = crcc.ca_crc([0x4, 0x3, 0x0, 0x5, 0x0, 0x1])
    print(crc_data10)
    ser = serial.Serial('/dev/ttyO1', 9600,timeout = 3)
    if ser.isOpen() :
        print("open success")
    else :
        print("open failed")
    while True:
        #send_data = input("input a data: ")
        #send_data = send_data + '\r\n'
        #serial.write(send_data.encode())
        sleep(1)
        #ser.write(bytes.fromhex(commidcode))
       
       
       
       
        ser.write([0x4, 0x3, 0x0, 0x5, 0x0, 0x1] + crc_data10)
        # 将16进制格式的字符串转化为16进制的字节数组
        data=ser.read(1)
        if data:
            sleep(0.1)
            n = ser.inWaiting()
            if n:
                data = data + ser.read(n)
        print(data)
        for i in data:
            print("%#x" % i)
        print(data[3:5])
        data4 = data[3:5]
        # 采用数组分割的方式获取光度值（16进制的数组）
        
        
        print(data4)
        print(int.from_bytes(data4, byteorder='big', signed=False))
        # 将16进制格式的字节数组转换为无符号整数
        
        data = ''
