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
    DMAH = 0x05
    DMAL = 0x06
    DMDI = 0x07
    VM0_reg  = 0x00
    VM1_reg  = 0x01

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

    def __init__(self):
        # Open a SPI port - max7456 connected on SPI0
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 500000
        self.spi.bits_per_word = 8
        self.spi.cshigh = False
        self.spi.lsbfirst = False
        self.spi.mode = 0

        # Set all rows at the same white level
        for x in range (0, self.MAX_screen_rows):
          self.spi.xfer2([(x + 0x10), self.WHITE_level_90])

        # Enable max7456
        self.spi.xfer2([self.VM0_reg, self.ENABLE_display]);

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
        self.spi.xfer2([self.VM0_reg, self.ENABLE_display]);
    
try:
    max7456 = max7456()
    max7456.testText()
    
except KeyboardInterrupt:
    spi.close() 

