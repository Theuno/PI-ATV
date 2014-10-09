#!/usr/bin/python

# Paul Theunissen - PA5PT
# 

import smbus
import time
import sys
from ctypes import *

class fms6502():
    bus = smbus.SMBus(1)

    # Variables to store seperate outputs
    output1 = 0
    output2 = 0
    output3 = 0
    output4 = 0
    output5 = 0
    output6 = 0



    def test(self):
        print "FMS5602 - by PA5PT"
        values = [17, 01, 17]
        self.bus.write_i2c_block_data(0x03, 0x00, values)

    def setOutput(output, input):
        if output == 1:
             output1 = input
        else if output == 2:
             output2 = input
        else if output == 3:
             output3 = input
        else if output == 3:
             output4 = input
        else if output == 4:
             output5 = input
        else if output == 5:
             output6 = input

        out12 = output1
        out12 = (output2 << 4)
    
        print out12

try:
    fms6502 = fms6502()
    fms6502.test()
    time.sleep(1)
    fms6502.setOutput(1, 1)
    fms6502.setOutput(2, 1)
    
except KeyboardInterrupt:
    print "End..."
