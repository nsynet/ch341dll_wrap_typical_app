import time
import ctypes

## call ch341dll_wrap
from ch341dll_32bits_wrap.ch341dll_wrap  import *

###1.  init ch341 device
hd = CH341DEV(0)
hd.ch341_i2c_speed(0)  #3=750Khz, 2=400k, 1=100k, 0=20k
write_data = [0]
data = (ctypes.c_byte * 5)()  # 创建一个ctypes数组

dht12_address = 0x5C

###2.  init 温湿度模块 DHT12
def read_dht12(address):
    global data  # 使用global声明，以便在函数内部修改data
    # 发送测量命令
    result=hd.ch341_stream_wi2c(address,write_data,5,data);
    time.sleep(2)  # 等待2秒再次读取

    # 读取数据
    # print("%d.%d.%d.%d.%d " % (data[0], data[1],data[2],data[3],data[4]))   #调试时打开打印
    
    # 校验数据
    if (result != 1) :
        return None, None, None, None
    if ((data[0] + data[1] +data[2]+data[3]) & 0xFF == data[4]):
        return data[0],data[1],data[2],data[3]
    else:
        return None, None, None, None


# 读取数据
while True:
    hum1, hum2,temp1 ,temp2 = read_dht12(dht12_address)
    if hum1 is not None and temp1 is not None and hum2 is not None and temp2 is not None:     
        print("湿度: %d.%d " % (hum1, hum2), end=' ')
        print("温度: %d.%d ℃" % (temp1, temp2))
    else:
        print("读取失败")



hd.ch341_close();