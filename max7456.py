#!/usr/bin/python

# Paul Theunissen - PA5PT
# 

import spidev
import time
from ctypes import *

# Open a SPI port - max7456 connected on SPI0
spi = spidev.SpiDev() 
spi.open(0, 0) 
spi.max_speed_hz = 500000
spi.bits_per_word = 8
spi.cshigh = False
spi.lsbfirst = False
spi.mode = 0

# MAX7456 opcodes
DMM_reg  = 0x04
DMAH_reg = 0x05
DMAL_reg = 0x06
DMDI_reg = 0x07
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

try:
  # Set all rows at the same white level
  for x in range (0, MAX_screen_rows):
    print "Row: ", x
    spi.xfer2([(x + 0x10), WHITE_level_90])

  # Enable max7456
  spi.xfer2([VM0_reg, ENABLE_display]);

  # Program test text
  x = 25
	
  spi.xfer2([0x05,0x01]) #DMAH

  spi.xfer2([0x06,x]) # DMAL
  spi.xfer2([0x07,0x1D])
	
  spi.xfer2([0x06,x+1]) # DMAL
  spi.xfer2([0x07,0x0B])
	
  spi.xfer2([0x06,x+2]) # DMAL
  spi.xfer2([0x07,0x17])
	
  spi.xfer2([0x06,x+3])
  spi.xfer2([0x07,0x1A])
	
  spi.xfer2([0x06,x+4])
  spi.xfer2([0x07,0x16])
	
  spi.xfer2([0x06,x+6])
  spi.xfer2([0x07,0x0F])
	
  # Enable display
  spi.xfer2([VM0_reg, ENABLE_display]);
    
except KeyboardInterrupt:
    spi.close() 

