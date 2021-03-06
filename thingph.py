#! /usr/bin/python
# -*- coding:utf-8 -*-

'''
Created on 2019-3-18

@author: 墨烦信息
'''

import sys
import time
import serial
import serial.tools.list_ports
import requests
from gpiozero import CPUTemperature

#處理、顯示數值    
def valueShow(argv):
    gzValue = '0x' + argv[12:14].replace(' ','')
    print(gzValue)
    return gzValue


# 發送訊號請求 PH 數值
def data_send(ser):
    #input_s = [1,3,0,2,0,2,101,203]  #0x01 0x03 0x00 0x00 0x00 0x02 0x65 0XCB
    input_s = [1,3,0,8,0,1,5,200]  #0x01 0x03 0x00 0x08 0x00 0x01 0x05 0XC8
    data = bytes(input_s)
    print("Data Sent:",data)
    ser.write(data)

# 接收 PH 數值
def data_receive(ser):
    try:
        num = ser.inWaiting()
    except:
        ser.close()
    if num > 0:
        data = ser.read(num)
        print("Data Receive: " , data)
        # hex显示
        out_s = ''
        for i in range(0, len(data)):
            out_s = out_s + '{:02X}'.format(data[i]) + ' '
        print("Output:",out_s)
        return valueShow(out_s)


if __name__ == '__main__':
    plist = list(serial.tools.list_ports.comports())
    #api_key = "0XW889E6RZV30F2H" #stempdummy
    #api_key = "2Y2R3NFQSI7LO419" #stempeduhk
    #api_key = "NOYMJU2NLMZNCLFG" #phValue

    cpu = CPUTemperature()
    
    if len(plist) <= 0:
        print("發現沒有連接!")
    else:
        plist_0 = list(plist[0])
        serialName = plist_0[0]
        ser = serial.Serial(serialName, 9600, timeout=0.5)
        print("連接 I/O", ser.name)
        while True:
            data_send(ser)
            time.sleep(2)
            returnValue = data_receive(ser)
            phValue = int(returnValue,16)
            
            #data= {"api_key":api_key,
            #       "field1":phValue,
            #       "field2":cpu.temperature}
            
            #res = requests.post("https://api.thingspeak.com/update.json",data=data)
            
            #print('PH VALUE:%.1f' % float(gzValue))
            print('PH: ',phValue/10)
            print('CPU TEMP: ', cpu.temperature)
            time.sleep(15)
        

    
