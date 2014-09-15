#!/usr/bin/python

# Paul Theunissen - PA5PT
# 

import spidev
import time
from ctypes import *

class max7456():
    # Create a SPI
    spi = spidev.SpiDev() 

    # MAX7456 opcodes
    DMM_reg  = 0x04
    DMAH     = 0x05
    DMAL     = 0x06
    DMDI     = 0x07
    VM0_reg  = 0x00
    VM1_reg  = 0x01
    HOS_reg  = 0x02
    STATUS   = 0xA0
    

    # PAL - VM0_reg commands
    ENABLE_display      = 0x48
    ENABLE_display_vert = 0x4c
    MAX7456_reset       = 0x42
    DISABLE_display     = 0x40

    MAX_screen_rows = 13

    # White levels
    WHITE_level_80  = 0x03
    WHITE_level_90  = 0x02
    WHITE_level_100 = 0x01
    WHITE_level_120 = 0x00

    chars = {' ':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
        '0':10, 'A':11, 'B':12, 'C':13, 'D':14, 'E':15, 'F':16, 'G':17, 'H':18, 'I':19,
        'J':20, 'K':21, 'L':22, 'M':23, 'N':24, 'O':25, 'P':26, 'Q':27, 'R':28, 'S':29,
        'T':30, 'U':31, 'V':32, 'W':33, 'X':34, 'Y':35, 'Z':36, 'a':37, 'b':38, 'c':39,
        'd':40, 'e':41, 'f':42, 'g':43, 'h':44, 'i':45, 'j':46, 'k':47, 'l':48, 'm':49,
        'n':50, 'o':51, 'p':52, 'q':53, 'r':54, 's':55, 't':56, 'u':57, 'v':58, 'x':59,
        'y':60, 'z':61, '(':62, ')':63, '.':64, '?':65, ';':66, ':':67, ',':68, '\'':69,
        '/':70, '"':71, '-':72, '&lt;':73, '&gt;':74, '@':75, '\xa9':76
    }

    def __init__(self):
        # Open a SPI port - max7456 connected on SPI0
        self.spi.open(0, 0)
        #self.spi.max_speed_hz = 500000
        #self.spi.max_speed_hz = 1000000
        print "Speed:", self.spi.max_speed_hz
        self.spi.bits_per_word = 8
        self.spi.cshigh = False
        self.spi.lsbfirst = False
        self.spi.mode = 0
  
        # On init, reset max7456
        self.reset()

        # Set all rows at the same white level
        for x in range (0, self.MAX_screen_rows):
          self.spi.xfer2([(x + 0x10), self.WHITE_level_90])

        # Enable max7456
        self.spi.xfer2([self.VM0_reg, self.ENABLE_display]);

    def printStr(self, Y, X, str, enable = True):
        disp = []
        for char in str:
            if self.chars.has_key(char):
                disp.append(self.chars[char])
            else:
                disp.append(0x00)
        disp.append(0xFF)

        start = Y * 30 + X
        self.spi.xfer2([self.VM0_reg, self.DISABLE_display])
        self.spi.xfer2([self.DMAL, start])
        self.spi.xfer2([self.DMM_reg, 0x01]) # TODO: Define
        print disp
        for char in disp:
            self.spi.xfer2([(char)])
        self.spi.xfer2([self.VM0_reg, self.ENABLE_display_vert])

    def reset(self):
        self.spi.xfer2([self.VM0_reg, self.MAX7456_reset])
        time.sleep(0.1)
        while True:
            r = self.spi.xfer([self.STATUS, 0x00])
            stable = self.testBit(r[1], 1)
            if stable == 0:
                print "Reset MAX7456 Ok..."
                break 
            time.sleep(0.2)
            print "Status: ", r
            break

    def testBit(self, int_type, offset):
        # TODO, move this function to a seperate class
        mask = 1 << offset
        return(int_type & mask)        

    def testText(self):
        # Program test text
        x = 25
	
        self.spi.xfer2([self.DMAH,0x01]) #DMAH

        self.spi.xfer2([self.DMAL,x]) # DMAL
        self.spi.xfer2([self.DMDI,0x1D])
	
        self.spi.xfer2([self.DMAL,x+1]) # DMAL
        self.spi.xfer2([self.DMDI,0x0B])
	
        self.spi.xfer2([self.DMAL,x+2]) # DMAL
        self.spi.xfer2([self.DMDI,0x17])
	
        self.spi.xfer2([self.DMAL,x+3])
        self.spi.xfer2([self.DMDI,0x1A])
	
        self.spi.xfer2([self.DMAL,x+4])
        self.spi.xfer2([self.DMDI,0x16])
	
        self.spi.xfer2([self.DMAL,x+5])
        self.spi.xfer2([self.DMDI,0x0F])
	
        # Enable display
        self.spi.xfer2([self.VM0_reg, self.ENABLE_display_vert]);

    
try:
    max7456 = max7456()
    #max7456.testText()
    
    # Use this line to align HOS and VOS
    max7456.printStr(0, 0, "012345678901234567890123456789")
    max7456.printStr(1, 0, "().                          .")
    max7456.printStr(2, 3, "Hello PA5PT")
    
except KeyboardInterrupt:
    spi.close() 

