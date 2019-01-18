# -*- coding: utf-8 -*- 
import serial
import os
from time import sleep


class IotLwm2m(object):
    """IotLwm2m 使用方法 """
    
    def __init__(self, name="aplex",serial_name = "/dev/ttyUSB0" ):
        self.name                   = name #公司的名字
        self.Power_on_init_list     = ["at+miplver?","AT+MIPLCREATE","AT+MIPLADDOBJ=0,3303,2,11,6,1","AT+MIPLADDOBJ=0,3306,1,1,5,0","AT+MIPLOPEN=0,3600,30"] # 
        self.ack_read_list          = [] #记录着OneNet平台下发的read请求的报文编号
        self.ack_write_list         = [] #记录着OneNet平台下发的read请求的报文编号
        self.ack_execture_list      = [] #记录着OneNet平台下发的read请求的报文编号
        self.ack_look_list          = [] #记录着OneNet平台下发的read请求的报文编号
        self.serial_name            = serial_name
        self.serial                 = ""
        
    def __str__(self):
        return "%s 公司的提供的iot通过lwm2m协议接入Onenet的方法" % (self.name, )

    def power_iot(self):
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
    
    def setup_serial(self,speed = 9600,readtimeout = 1):
        self.serial = serial.Serial(self.serial_name, speed,timeout = readtimeout)
        if self.serial.isOpen():
            print("open success")
        else:
            print("open failed")
            
    
    def auto_connect(self):
        for list in self.Power_on_init_list:
            cmd_iot = list + "\r\n"
            self.serial.write(cmd_iot.encode())
            data = self.serial.read_all().decode()
            print (data)
            sleep (1)
            
            
    def ack_iot(self):   #iot终端向onenet平台的回复信息
        sleep(0.5)
        data = self.serial.read_all().decode()
        send_data               =    ""
        #print("recv:"+data)
        
        #ack_data[1]表示当前来自云平台的报文id
        if "+MIPLOBSERVE:" in data:  #询问有没有这个实例
            ack_data = data.split(',')
            #print(ack_data)
            
            send_data = "AT+MIPLOBSERVERSP=0,%s,1\r\n" % (ack_data[1],)
            self.serial.write(send_data.encode())
            sleep(0.5)
            
        elif "+MIPLDISCOVER:" in data:  #询问类型的成员
            ack_data = data.split(',')
            #'+MIPLDISCOVER: 0', 
            #'61245', 
            #'3303\r\n'
            ack_data[2]    = ack_data[2][0:4]
            #print(ack_data)
            #在这里根据对象类型的文档将对象类型的结构提前定义好，这里以3303对象类型为例
            if ack_data[2] == "3303":
                send_data = 'AT+MIPLDISCOVERRSP=0,%s,1,34,"5700;5701;5601;5602;5603;5604;5605"\r\n' % (ack_data[1],)
            elif ack_data[2] == "3306":
                send_data = 'AT+MIPLDISCOVERRSP=0,%s,1,24,"5850;5851;5852;5853;5750"\r\n' % (ack_data[1],)

            #print(send_data)
            self.serial.write(send_data.encode())
            sleep(0.5)
            
        elif "+MIPLREAD:" in data:  #通知读取结果
            
            print("recv:"+data)
            ack_data                 = data.split(',')
            #recv:+MIPLREAD: 0,
            #4932,
            #3303,
            #0,
            #5700
            print(ack_data)
            ack_data[4]    = ack_data[4][0:4]
            print (ack_data[2],ack_data[4])
            if ack_data[2]          ==   "3303" :
                if ack_data[4]      ==   "5700" :
                    send_data       =    'AT+MIPLREADRSP=0,%s,1,%s,%s,%s,4,4,20.123,0,0\r\n' % (ack_data[1],ack_data[2],ack_data[3],ack_data[4])
                elif ack_data[4]    ==   "5701" :
                    send_data       =    'AT+MIPLREADRSP=0,%s,1,%s,%s,%s,1,5,aplex,0,0\r\n' % (ack_data[1],ack_data[2],ack_data[3],ack_data[4])
                elif ack_data[4]    ==   "5601" :
                    send_data       =    'AT+MIPLREADRSP=0,%s,1,%s,%s,%s,4,4,20.135,0,0\r\n' % (ack_data[1],ack_data[2],ack_data[3],ack_data[4])
                elif ack_data[4]    ==   "5602" :
                    send_data       =    'AT+MIPLREADRSP=0,%s,1,%s,%s,%s,4,4,80.123,0,0\r\n' % (ack_data[1],ack_data[2],ack_data[3],ack_data[4])   
                elif ack_data[4]    ==   "5603" :
                    send_data       =    'AT+MIPLREADRSP=0,%s,1,%s,%s,%s,4,4,44.55,0,0\r\n' % (ack_data[1],ack_data[2],ack_data[3],ack_data[4])
                elif ack_data[4]    ==   "5604" :
                    send_data       =    'AT+MIPLREADRSP=0,%s,1,%s,%s,%s,4,4,55.66,0,0\r\n' % (ack_data[1],ack_data[2],ack_data[3],ack_data[4])
                elif ack_data[4]    ==   "5605" :
                    send_data       =    'AT+MIPLREADRSP=0,%s,1,%s,%s,%s,2,3,zwd,0,0\r\n' % (ack_data[1],ack_data[2],ack_data[3],ack_data[4])
            if ack_data[2]          ==   "3306" :
                if ack_data[4]      ==   "5853" :
                        send_data       =    'AT+MIPLREADRSP=0,%s,1,%s,%s,%s,1,5,aplex,0,0\r\n' % (ack_data[1],ack_data[2],ack_data[3],ack_data[4])
            self.serial.write(send_data.encode())
            sleep(0.5)
        elif "+MIPLWRITERSP:" in data:  #通知写入的消息结果
            print("recv:"+data)
            ack_data = data.split(',')
            send_data = 'AT+MIPLREADRSP=0,%s,1,3303,0,5700,4,4,20.123,0,0' % (ack_data[1],)
            print(send_data)
            self.serial.write(send_data.encode())
        elif "+MIPLEXECUTERSP:" in data:  #通知执行操作果
            print("recv:"+data)
            ack_data = data.split(',')
            send_data = 'AT+MIPLREADRSP=0,%s,1,3303,0,5700,4,4,20.123,0,0' % (ack_data[1],)
            print(send_data)
            self.serial.write(send_data.encode())
        elif "+MIPLOBSERVERSP:" in data:  #通知观测指令是否有效
            print("recv:"+data)
            ack_data = data.split(',')
            send_data = 'AT+MIPLREADRSP=0,%s,1,3303,0,5700,4,4,20.123,0,0' % (ack_data[1],)
            print(send_data)
            self.serial.write(send_data.encode())
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
    iot_lwm2m = IotLwm2m()
    iot_lwm2m.power_iot()
    iot_lwm2m.setup_serial()
    iot_lwm2m.auto_connect()
    while True:
        iot_lwm2m.ack_iot()