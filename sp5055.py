#!/usr/bin/python

import time
import smbus
import sys
from ctypes import *

class PLL:
  #Enable/Disable debugging
  debugLib = False

  # I2C bus
  bus = smbus.SMBus(1)

  # Default frequency (2335 is PI6EHV pip3, 2367 is PI6EHV pip4)
  defFreq = 2335
  lock = False
  lockTime = 0
  Xtall = c_ulong(4000)
  address = 0x60

  def __init__(self):
      print " [ SP5055 Controller for Raspberry PI ] "
      print " [ by Paul Theunissen - PA5PT         ] "

  def readLock(self):
      status = self.bus.read_byte(0x61)
      print "SP5055 Status: " + str(status)
      lockBit = status & 0x40
      if lockBit == 64:
        return True
      else:
        return False

  def switchToDefaultFreq(self):
      switchToFreq(defFreq)

  def switchToFreq(self, freq):
      f = c_ulong(freq * 4 * 2)
      if self.debugLib == True:
          print "---------------------------"
          print "Target frequency: " + str(freq)
          print "f: " + str(f.value)

      a = c_ulong((f.value >> 8))
      a = c_ulong(a.value & 0x7F)
      a = chr(a.value)
      b = c_ulong(f.value & 0xFF)
      b = chr(b.value)
      # Charge pump different for some boards?
      #c = chr(0b11111110)
      c = chr(0xCE)
      d = chr(0b00000000)
      
      if self.debugLib == True:
          print "[ Sending: ]" 
          print a.encode("hex")
          print b.encode("hex")
          print c.encode("hex")
          print d.encode("hex")

      # Send
      values = [ord(b), ord(c), ord(d)]
      self.bus.write_i2c_block_data(self.address, ord(a), values)
      time.sleep(1)

  def waitForLock(self):
      while self.lock != True:
        if self.readLock() == True:
          self.lock = True
          self.lockTime = time.time()
          print "Locked at: " + str(self.lockTime)
          time.sleep(2)
        else:
          print "Not yet locked"
          time.sleep(2)

board = PLL()
#board.switchToDefaultFreq()
if len(sys.argv) > 1:
    print sys.argv
    board.switchToFreq(int(sys.argv[1]))
else:
    board.switchToFreq(2367)
board.waitForLock()
