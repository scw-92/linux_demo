# -*- coding: utf-8 -*- 
import serial
import os
from time import sleep


#list_iot = ["at+miplver?","AT+MIPLCREATE=51,130033f10003f20021050011000000000000000d3138332e3233302e34302e333900044e554c4cf3000cea040000044e554c4c,0,51,0","AT+MIPLADDOBJ=0,3303,2,11,7,3","AT+MIPLOPEN=0,3600,30"]
list_iot = ["at+miplver?","AT+MIPLCREATE","AT+MIPLADDOBJ=0,3303,2,11,7,3","AT+MIPLOPEN=0,3600,30"]

#sim70920c 向移动云平台注册通信套件的步骤

observe_list=[]  #记录着OneNet平台下发的discover请求的报文编号

def auto_connect(serial,cmd_iot):
    serial.write(cmd_iot.encode())
    data = serial.read_all().decode()
    print(data)
    sleep(1)

def ack_iot(serial):   #iot终端向onenet平台的回复信息
   
    sleep(0.5)
    data = serial.read_all().decode()
    #print("recv:"+data)
	
	#ack_data[1]表示当前来自云平台的报文id
    if "+MIPLOBSERVE:" in data:
        ack_data = data.split(',')
        #print(ack_data)
        observe_list.append(ack_data[1])
        send_data = "AT+MIPLOBSERVERSP=0,%s,1\r\n" % (ack_data[1],)
        serial.write(send_data.encode())
        sleep(0.5)
		#跟云平台确认对象的存在
		
    elif "+MIPLDISCOVER:" in data:
        ack_data = data.split(',')
        # print(ack_data)
        
        send_data = 'AT+MIPLDISCOVERRSP=0,%s,1,34,"5700;5701;5601;5602;5603;5604;5605"\r\n' % (ack_data[1],)
        
        #send_data = 'AT+MIPLDISCOVERRSP=0,%s,1,34,"5700;5701;5601;5602;5603;5604;5605"\r\n' % (ack_data[1],)

        #print(send_data)
        serial.write(send_data.encode())
        sleep(0.5)
    elif "+MIPLREAD:" in data:  #通知读取结果
        print("recv:"+data)
        ack_data = data.split(',')
        
        send_data = 'AT+MIPLREADRSP=0,%s,1,3303,0,5701,1,3,zwd,0,0\r\n' % (ack_data[1],)
        
        #print(send_data)
        serial.write(send_data.encode())
        sleep(0.5)
    elif "+MIPLWRITERSP:" in data:  #通知写入的消息结果
        print("recv:"+data)
        ack_data = data.split(',')
        send_data = 'AT+MIPLREADRSP=0,%s,1,3303,0,5700,4,4,20.123,0,0' % (ack_data[1],)
        print(send_data)
        serial.write(send_data.encode())
    elif "+MIPLEXECUTERSP:" in data:  #通知执行操作果
        print("recv:"+data)
        ack_data = data.split(',')
        send_data = 'AT+MIPLREADRSP=0,%s,1,3303,0,5700,4,4,20.123,0,0' % (ack_data[1],)
        print(send_data)
        serial.write(send_data.encode())
    elif "+MIPLOBSERVERSP:" in data:  #通知观测指令是否有效
        print("recv:"+data)
        ack_data = data.split(',')
        send_data = 'AT+MIPLREADRSP=0,%s,1,3303,0,5700,4,4,20.123,0,0' % (ack_data[1],)
        print(send_data)
        serial.write(send_data.encode())
    else:
        print(data)
		#上报云平台对象的内部结构
'''      
        data = serial.read_all().decode()
        print(observe_list[0]) 
        send_data = "AT+MIPLNOTIFY=0,%s,3303,0,5700,4,2,34,0,0,0\r\n" % (observe_list[0],)
        print(send_data)
        serial.write(send_data.encode())
        data = serial.read_all().decode()
'''
	
if __name__ == '__main__':
    #os.system('echo 19 > /sys/class/gpio/export')
    #os.system('echo out > /sys/class/gpio/gpio19/direction')
    os.system('echo 1 > /sys/class/gpio/gpio19/value')
    os.system('sleep 1')
    os.system('echo 0 > /sys/class/gpio/gpio19/value')
    sleep (2)

    os.system('echo 1 > /sys/class/gpio/gpio19/value')
    os.system('sleep 1')
    os.system('echo 0 > /sys/class/gpio/gpio19/value')
    sleep(8)
    serial = serial.Serial('/dev/ttyUSB0', 9600,timeout=1)
    if serial.isOpen() :
         print("open success")
    else :
        print("open failed")

    for i in list_iot:
        auto_connect(serial,i+"\r\n")
    while True:
        ack_iot(serial)

