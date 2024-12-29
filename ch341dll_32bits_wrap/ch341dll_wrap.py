import ctypes

## only win32 version python can Load the CH341DLL.dll
ch341dll = ctypes.windll.LoadLibrary(".//CH341DLL_31k.dll")
print("Ch341dll_wrap is loaded!!! only work for python 32bits version !!!")
class CH341DEV():
    def __init__(self, dev_index = 0):
        self.usb_id = dev_index
        self.open_status = 0;
        self.i2c_speed = 3;
        self.ch341_open();
        self.ch341_i2c_speed(self.i2c_speed);

    def check_status (self):
        if (self.open_status == 0):
            print("Open USB CH341Dev Index=",self.usb_id," is not ready, pls try to open it firsit!!!!!!!")
            return -1;

        return 1;

    def ch341_open(self ):
        if ( ch341dll.CH341OpenDevice(self.usb_id) > 0):
            print("Open USB CH341Dev Index=",self.usb_id,"ok!!!!!!!")
            self.open_status = 1;
            return self.usb_id;
        else:
            print("Error!!! USB CH341 Open Failed!")
            self.open_status = 0;
            return -1

    def ch341_close(self):
        if (ch341dll.CH341CloseDevice(self.usb_id) > 0):
            print("Close USB CH341Dev Index=", self.usb_id, "ok!!!!!!!")
            self.open_status = 0;
            return 1;
        else:
            print("Error!!! USB CH341 Close Failed!")
            return -1

    def ch341_i2c_speed(self,speed=3):
        self.i2c_speed = speed;
        if(self.check_status() < 1):
            print ("set I2C speed to ", speed, "Fail ,please check your CH341 Device !!")
            return -1;
        if (ch341dll.CH341SetStream(self.usb_id,0x80+speed) > 0):
            print ("set I2C speed to ", speed, "(3=750Khz, 2=400k, 1=100k, 0=20k")
            return 1;
        else:
            self.open_status = 0;
            print ("set I2C speed to ", speed, "Fail ,please check your CH341 Device !!")
            return -1

    def ch341_swi2c (self,i2c_addr7b,reg_addr,wdata):
        if(self.check_status() < 1):
            return -1;
        return ch341dll.CH341WriteI2C(self.usb_id, i2c_addr7b & 0xff, reg_addr&0xff, wdata&0xff)

    def ch341_sri2c (self,i2c_addr7b,reg_addr):
        if(self.check_status() < 1):
            return -1;
        rdata = (ctypes.c_uint8 * 1)()
        if( ch341dll.CH341ReadI2C(self.usb_id, i2c_addr7b & 0xff, reg_addr&0xff,rdata ) > 0):
            return rdata[0]&0xff
        else:
            return -1;

    def ch341_stream_wi2c (self,i2c_addr7b,din):
        '''i2c rw stream '''
        if(self.check_status() < 1):
            return -1;
        inlen = len(din);
        if inlen > 4000:
            print("should not greater than 4000");
            return -1;
        inlen += 1;
        wdata = (ctypes.c_uint8 * (inlen))()
        rdata = (ctypes.c_uint8 * (inlen))()
        wdata[0] = (i2c_addr7b & 0xff) << 1;
        for ii in range(1,inlen):
            wdata[ii] = din[ii-1] & 0xff;
        #print("debug: wlen=",inlen)
        #print("debug: wdata=",wdata[100:])
        if( ch341dll.CH341StreamI2C (self.usb_id, inlen, wdata ,0, rdata ) > 0):
            return 1;
        else:
            return -1;

    def ch341_stream_wi2c (self,i2c_addr7b,din,read_len,read_data):
        '''i2c rw stream '''
        if(self.check_status() < 1):
            return -1;
        inlen = len(din);
        if inlen > 4000:
            print("should not greater than 4000");
            return -1;
        inlen += 1;
        wdata = (ctypes.c_uint8 * (inlen))()
        wdata[0] = (i2c_addr7b & 0xff) << 1;
        for ii in range(1,inlen):
            wdata[ii] = din[ii-1] & 0xff;
        if( ch341dll.CH341StreamI2C (self.usb_id, inlen, wdata ,read_len, read_data ) > 0):
            return 1;
        else:
            return -1;


    def spi_oled1306_3w(self, not_cmd, data):
        if (self.check_status() < 1):
            return -1;
        wdata = (ctypes.c_uint8 * 2)()
        wdata[0] = (( not_cmd & 0x1 ) << 7) + (data >> 1);
        wdata[1] = (data & 1)<<7;
        if (ch341dll.CH341StreamSPI4(self.usb_id, 0x80, 2, wdata)):
            return 1
        else:
            return -1;

    def ch341_spi4w_stream(self,din):
        if(self.check_status() < 1):
            return -1;
        inlen = len(din);
        if inlen > 4000:
            print("should not greater than 4000");
            return -1;
        wdata = (ctypes.c_byte* (inlen))()
        for ii in range(inlen):
            wdata[ii] = int(din[ii]) & 0xff;
        #print("debug: wlen=",inlen)
        #print("debug: wdata=",wdata[100:])
        #print("debug: get_inptus: ",din,"length = ",len(din), inlen);
        if (ch341dll.CH341StreamSPI4(self.usb_id, 0x80, inlen, wdata)):
            return wdata;
        else:
            return -1;

    def ch341_get_input(self):
        if(self.check_status() < 1):
            return -1;
        inlen = 4
        rdata = (ctypes.c_byte* (inlen))()
        for ii in range(inlen):
            rdata[ii] = 0;
        if (ch341dll.CH341GetInput(self.usb_id, rdata)):
            return (rdata[0] + rdata[1]*256 + rdata[3]*256);
        else:
            return -1;

    def ch341_set_output(self,set_range, set_dir, set_v):
        if(self.check_status() < 1):
            return -1;
        if (ch341dll.CH341SetOutput(self.usb_id, set_range,set_dir, set_v)):
            return 1;
        else:
            return -1;

    def ch341_oled306_3w_stream(self,din):
        if(self.check_status() < 1):
            return -1;
        inlen = len(din);
        if inlen > 4000:
            print("should not greater than 4000");
            return -1;
        wdata = (ctypes.c_byte* (inlen))()
        rdata = (ctypes.c_byte* (inlen))()
        for ii in range(inlen):
            wdata[ii] = int(din[ii]) & 0xff;
        #print("debug: wlen=",inlen)
        #print("debug: wdata=",wdata[100:])
        #print("debug: get_inptus: ",din,"length = ",len(din), inlen);
        if (ch341dll.CH341StreamSPI4(self.usb_id, 0x80, inlen, wdata)):
            return 1;
        else:
            return -1;

if __name__ == "__main__":
    hd = CH341DEV(0)
    #hd.ch341_close()
    xx = hd.ch341_get_input();
    yy = xx & 0xff
    print("get_input GPIO date D7:D0:", hex(yy))
    hd.ch341_close();
