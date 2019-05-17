#! /usr/bin/python
# -*- coding:utf-8 -*-

'''
Created on 2019-3-18

@author: STEMP Technology
'''

import sys
import time
import serial
import serial.tools.list_ports

#處理光照值   
def valueShow(argv):
    luxValue = '0x' + argv[8:20].replace(' ','')
    return luxValue 

#處理、顯示溫度、濕度
def tempShow(argv):
    humidityValue = '0x' + argv[8:14].replace(' ','')    #從數據中獲得溫度數據
    tempValue  = '0x' + argv[14:20].replace(' ','')  #从返回數據中獲得濕度數據
    print('温度:',tempValue,'湿度:',humidityValue)      #顯示结果，檢查是否正確
    return tempValue,humidityValue

# 要求光照值數據
def data_send(ser):
    input_s = [1,3,0,2,0,2,101,203]  #0x01 0x03 0x00 0x00 0x00 0x02 0x65 0XCB
    data = bytes(input_s)
    print("Data Sent:",data)
    ser.write(data)

#要求溫度、濕度數據
def data_send_temp(ser):
    input_s = [1,3,0,0,0,2,196,11] #0x01 0x03 0x00 0x00 0x00 0x02 0xC4 0X0B
    data = bytes(input_s)
    print("Data Sent:",data)
    ser.write(data)
        
# 接收光照数据
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
        print("Output: ",out_s)
        return valueShow(out_s)

# 接收溫度、濕度數據
def data_receive_temp(ser):
    try:
        num = ser.inWaiting()
    except:
        ser.close()
    if num > 0:
        data = ser.read(num)
        print("Data Receive: ",data)
        # hex显示
        out_s = ''
        for i in range(0, len(data)):
            out_s = out_s + '{:02X}'.format(data[i]) + ' '
        print("Output: ", out_s)
        return tempShow(out_s)       

if __name__ == '__main__':
    plist = list(serial.tools.list_ports.comports())
    
    if len(plist) <= 0:
        print("發現沒有連接!")
        conn.close()
    else:
        plist_0 = list(plist[0])
        serialName = plist_0[0]
        ser = serial.Serial(serialName, 9600, timeout=0.5)
        print("連接 I/O", ser.name)
        while True:
            data_send(ser)
            time.sleep(1)
            gzValue = int(data_receive(ser),16)
            data_send_temp(ser)
            time.sleep(1)
            tempValue,humValue = data_receive_temp(ser)

            print('Lux:%.1f' % float(gzValue))
            print('Temp:%.1f' % float(int(tempValue,16)/10))
            print('Humidity:%.1f' % float(int(humValue,16)/10))
            time.sleep(1)
        

    
