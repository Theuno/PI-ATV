#!/usr/bin/python

import time
from Adafruit_I2C import *

class PLL:
  #Enable/Disable debugging of the Adafruit I2C Library
  debugLib = True

  defFreq = 2335

  i2cRead = Adafruit_I2C(0x60, debug=debugLib)
  i2cWrite = Adafruit_I2C(0x61, debug=debugLib)

  def __init__(self):
      print " [ SP5055 Controller for Raspberry PI ] "
      print " [ by Paul Theunissen - PA5PT         ] "
    
      print " Initialize PLL: "
      self.initPLL()

  def initPLL(self):
      print "..."
#      lijst = [0x80]
#      self.i2cWrite.writeList(0x48, lijst)
      print "[OK]"

  def readStatus(self):
      print "Reading PLL Status"
      status = self.i2cRead.readU8(0x48)
      print "Status: " + str(status)
      return status

  def switchToDefaultFreq(self):
      # <TODO>
      print "Setting to default frequency: " + str(self.defFreq)
      lijst = [0x80]
      status = self.i2cWrite.writeList(0x48, lijst)
      # print "Result: " + status
      time.sleep(1) 
      #sudo i2cset -y 1 0x61 0x48 0x80

  def waitForLock(self):
      status = self.readStatus()
      #print "Current status: " + str(status)
      while status != 64:
        time.sleep(2)
        status = self.readStatus()
        print "Current status: " + str(status)

board = PLL()
board.readStatus()
board.switchToDefaultFreq()
board.waitForLock()
