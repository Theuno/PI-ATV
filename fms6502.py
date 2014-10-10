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

    def LoadDefaults(self,filename='FMS6502.json'):
        try:
            f=open(filename,'r')
            Defaults=json.load(f)
            f.close()
            Loaded=True
        except:
            Loaded=False
        if Loaded:
            print "TODO"
            #for i in Defaults['inputs']:
            #    self.Input[i['Input']].SetClamp(i['Clamp'])
            #for i in Defaults['outputs']:
            #    self.Output[i['Output']]._Enable = i['Enable']
            #    self.Output[i['Output']]._Gain = i['Gain']
            #    self.Output[i['Output']]._Source = i['Source']
            #    self.Output[i['Output']]._Update()

    def test(self):
        print "FMS5602 - by PA5PT"
        values = [17, 01, 17]
        self.bus.write_i2c_block_data(0x03, 0x00, values)

    def setOutput(self, output, input):
        if input > 8:
             print "[ERROR] There are only 8 inputs"
        if output > 6:
             print "[ERROR] There are only 6 outputs"

        if output == 1:
             self.output1 = input
        if output == 2:
             self.output2 = input
        if output == 3:
             self.output3 = input
        if output == 3:
             self.output4 = input
        if output == 4:
             self.output5 = input
        if output == 5:
             self.output6 = input
        
        out12 = [self.output1]
        out12[0] = out12[0] | (self.output2 << 4)
        out34 = [self.output3]
        out34[0] = out34[0] | (self.output4 << 4)
        out56 = [self.output5]
        out56[0] = out56[0] | (self.output6 << 4)
    
        print "Output12 register: " + str(out12[0])
        print "Output34 register: " + str(out34[0])
        print "Output56 register: " + str(out56[0])

        self.bus.write_i2c_block_data(0x03, 0x00, out12)
        self.bus.write_i2c_block_data(0x03, 0x01, out34)
        self.bus.write_i2c_block_data(0x03, 0x02, out56)


try:
    fms6502 = fms6502()
    fms6502.test()
    time.sleep(1)
    fms6502.setOutput(1, 6)
    fms6502.setOutput(2, 6)
    fms6502.setOutput(3, 5)
    fms6502.setOutput(4, 6)
    #fms6502.setOutput(5, 5)
    #fms6502.setOutput(6, 5)
   
# Input:
# 1 - External 1
# 2 - External 2
# 3 - External 3
# 4 - External 4
# 5 - Raspberry Pi
# 6 - MAX7456
# 7 - 
# 8 - 
#
# Output:
# 1 - External 1
# 2 - External 2
# 3 - MAX7456
# 4 - Baseband Modulator
 
except KeyboardInterrupt:
    print "End..."
