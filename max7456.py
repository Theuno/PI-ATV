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
    VM0_reg  = 0x00
    VM1_reg  = 0x01
    HOS_reg  = 0x02
    VOS_reg  = 0x03
    DMM_reg  = 0x04
    DMAH     = 0x05
    DMAL     = 0x06
    DMDI     = 0x07
    OSDM     = 0x0C
    RB0      = 0x10
    HOS_reg  = 0x02
    STATUS   = 0xA0

    # PAL - VM0_reg commands
    ENABLE_display      = 0x48
    ENABLE_display_vert = 0x4c
    MAX7456_reset       = 0x42
    DISABLE_display     = 0x40

    # Read command
    READ = 0x80

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
          self.spi.xfer2([(self.RB0 + x), self.WHITE_level_90])

        # Enable max7456
        self.spi.xfer2([self.VM0_reg, self.ENABLE_display]);

    def printStr2(self, Y, X, str, enable = True):
        disp = []
        for char in str:
            if self.chars.has_key(char):
                disp.append(self.chars[char])
            else:
                disp.append(0x00)
        disp.append(0xFF)

        start = X * 30 + Y
        self.spi.xfer2([self.VM0_reg, self.DISABLE_display])
        self.spi.xfer2([self.DMAL, start])
        self.spi.xfer2([self.DMM_reg, 0x01]) # TODO: Define
        print disp
        for char in disp:
            self.spi.xfer2([(char)])
        self.spi.xfer2([self.VM0_reg, self.ENABLE_display_vert])

    def printStr(self, X, Y, string, enable = True, blink = False, invert = False):
        disp = []
        for char in string:
            if self.chars.has_key(char):
                disp.append(self.chars[char])
            else:
                disp.append(0x00)
        # Append break character
        #disp.append(0xFF)
        print string
        print disp

        if enable == True:
            self.spi.xfer([self.VM0_reg, self.DISABLE_display])
        
        # Enable 8 bit mode:
        dmm = self.spi.xfer2([self.DMM_reg + self.READ, 0x00])
        print "DMM before: ", dmm
        dmm = self.setBit(dmm[1], 6)
        print "DMM After: ", dmm
        self.spi.xfer2([self.DMM_reg, dmm]) # TODO: Define...

        start = X * 30 + Y
        # Clear position
        self.spi.xfer2([self.DMAH, 0x00])
        self.spi.xfer2([self.DMAL, 0x00])

        for char in disp:
            # Write char
            dmah = self.spi.xfer2([self.DMAH + self.READ, 0x00])
            dmah = self.clearBit(dmah[1], 1)
            self.spi.xfer2([self.DMAH, dmah])

            dmah_pos = ((start >> 8) & 0x01)
            dmal = (start & 0xff)
            dmah = dmah | dmah_pos
            print "printStr2 (start, dmah, dmal): ", start, dmah, dmal
            start = start + 1

            # Select MSB
            self.spi.xfer2([self.DMAH, dmah])
            self.spi.xfer2([self.DMAL, dmal])
        
            self.spi.xfer2([self.DMDI, (char)])
            
            # Set DMAH to 1 to write attributes (blink, invert)
            attrib = False
 
            if blink == True | invert == True: 
                dmah = self.spi.xfer2([self.DMAH + self.READ, 0x00])
                dmah = self.setBit(dmah[1], 1)
                dmah = self.spi.xfer2([self.DMAH, dmah])
                
                # Write DMDI
                dmdi = self.spi.xfer2([self.DMDI + self.READ, 0x00])
                dmdi = dmdi[1]
                dmdi = 0x00

                if blink == True:
                    dmdi = self.setBit(dmdi, 6)
                if invert == True:
                    dmdi = self.setBit(dmdi, 5)
                # Local background, is at bit 4

                self.spi.xfer2([self.DMDI, dmdi])
                

        if enable == True:
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

    def getHos(self):
        hos = self.spi.xfer2([self.HOS_reg + self.READ, 0x00])
        return hos[1]
    
    def setHos(self, value):
        self.spi.xfer2([self.HOS_reg, value])

    def getVos(self):
        vos = self.spi.xfer2([self.VOS_reg + self.READ, 0x00])
        return vos[1]

    def setVos(self, value):
        self.spi.xfer2([self.VOS_reg, value])

    def testBit(self, value, offset):
        # TODO, move this function to a seperate class
        mask = 1 << value
        return(value & mask)
 
    def setBit(self, value, offset):
        # TODO, move this function to a seperate class
        mask = 1 << offset
        return(value + mask)

    def clearBit(self, int_type, offset):
        # TODO, move this function to a seperate class
        mask = ~(1 << offset)
        return(int_type & mask)

    # Sample function to quickly test the MAX7456 (After init)
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
    max7456.printStr(0, 0,  "012345678901234567890123456789")
    hos = max7456.getHos()
    hos = hos - 1
    max7456.setHos(hos)


    max7456.printStr2(2, 3, "Write text in 16 bit mode.....")
    time.sleep(1)
    max7456.printStr(0, 0,  "012345678901234567890123456789")
    max7456.printStr(1, 0,  "1                            1")
    max7456.printStr(2, 0,  "2                            2")
    max7456.printStr(3, 0,  "3                            3")
    max7456.printStr(4, 0,  "4                            4")
    max7456.printStr(5, 0,  "5                            5")
    max7456.printStr(6, 0,  "6                            6")
    max7456.printStr(7, 0,  "7                            7")
    max7456.printStr(8, 0,  "8                            8")
    max7456.printStr(9, 0,  "9                            9")
    max7456.printStr(10, 0, "10                          10")
    max7456.printStr(11, 0, "11                          11")
    max7456.printStr(12, 0, "12                          12")
    max7456.printStr(13, 0, "13                          13")
    max7456.printStr(14, 0, "14                          14")
    max7456.printStr(15, 0, "15                          15")

    time.sleep(2)
    max7456.printStr(7,10, "Hello PA5PT", enable = False, blink = True, invert = True)
    
except KeyboardInterrupt:
    spi.close() 

