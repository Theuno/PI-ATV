#!/usr/bin/python

# Paul Theunissen - PA5PT
# 

import smbus
import time
import sys
from ctypes import *

class fms6502():
    bus = smbus.SMBus(1)

    def test(self):
        print "FMS5602 - by PA5PT"
        values = [17, 01, 17]
        self.bus.write_i2c_block_data(0x03, 0x00, values)


    
try:
    fms6502 = fms6502()
    fms6502.test()
    time.sleep(1)
    
except KeyboardInterrupt:
    print "End..."
