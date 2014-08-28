#!/usr/bin/python

# Paul Theunissen - PA5PT
# This file uses functions from BitWizard libraries and is meant to be used with;
# http://www.bitwizard.nl/shop/raspberry-pi-ui-16x2
# BitWizard files required can be found: https://github.com/rewolff/bw_library
# 

from BitWizard.bw import *
from BitWizard.ui import *
import struct

import pygame
from pygame.locals import *
import time
import os
import sys
import random
import glob

class Generator():
    ''' This class is based on an example from PA3BWE - http://pa3bwe.milatz.nl/?p=88 '''
    ''' Improvements were made by PE9ZZ - http://www.atvin.nl/forum/index.php?topic=364.0 '''
    # screen size
    size_h = 768
    size_v = 576

    #misc paths
    atv_media_path = '/home/pi/atv/images'
 
    images = []
    i = 0
    screen = 0
    currentimage = os.path.join(atv_media_path,"image01.jpg")

    def __init__(self):
        self.images = sorted(glob.glob(os.path.join(self.atv_media_path,"*.jpg")))
        print self.images

        textOn = False
        stepX = 10
        stepY = 10

	# Init PyGame
        print "Init PyGame"
        pygame.init()
        pygame.mixer.init(44000, -16, 1, 1024)
        pygame.mouse.set_visible (0)

        pygame.time.set_timer(pygame.USEREVENT, 15000)
        self.screen = pygame.display.set_mode((self.size_h,self.size_v),pygame.FULLSCREEN)

        self.update_screen()
        running = True
        clock = pygame.time.Clock()

    def __del__(self):
        pygame.quit()
        pygame.mixer.quit()


    # load image
    def loadimage(self):
        testimage = os.path.join(atv_media_path,"image" + s + ".jpg")
        try:
                with open(testimage) as f:
                        self.currentimage = testimage
        except:
                pass

    # Next image
    def next_image(self):
        print "Next: ", self.i
        print "Length: ", len(self.images)
        if (self.i + 1) < len(self.images):
            self.i = self.i + 1
            self.changeImage(self.i)
        else:
            print "Last image..."

    def previous_image(self):
        print "Previous: ", self.i
        if 0 < self.i:
            self.i = self.i - 1
            self.changeImage(self.i)
        else:
            print "First image..."

    def changeImage(self, image):
        print "Image: ", self.images[image]
        testimage = self.images[image]
        try:
                with open(testimage) as f:
                        self.currentimage = testimage
        except:
                print "Problem"
                pass


    #update screen
    def update_screen(self, screen = None, update = True):
        if screen is None:
            screen = self.screen
        picture = pygame.image.load(self.currentimage)
        screen.blit(picture, (0,0))

        if update:
                pygame.display.update()


    def Show(self,menu):
        menu.Display.Print("Set picture")
        menu.Display.SetCursor(0,1)
        menu.Display.Print("Value:")
        menu.Display.Cursor(False,False)
        while not menu.Buttons.ReportPressed()[menu.ButtonEsc]:
            value = 1
            menu.Display.SetCursor(menu.Display.Width-len("%4d" % value),1)
            menu.Display.Print("%4d"% value)

            if menu.Buttons.ReportPressed()[menu.ButtonLeft]:
                self.previous_image()
                self.update_screen()
                print 'Value: ',value
                menu.Display.SetCursor(menu.Display.Width-len("%4d" % value),1)
                menu.Display.Print("%4d"% value)
            if menu.Buttons.ReportPressed()[menu.ButtonRight]:
                self.next_image()
                self.update_screen()
                print 'Value: ',Generator.i
                menu.Display.SetCursor(menu.Display.Width-len("%4d" % value),1)
                menu.Display.Print("%4d"% value)
            sleep(.2)




class ContrastMenu():
    ''' Should move to seperate file '''
    def __init__(self):
        pass

    @staticmethod
    def Show(menu):
        menu.Display.Print("Set contrast")
        menu.Display.SetCursor(0,1)
        menu.Display.Print("Value:")
        menu.Display.Cursor(False,False)
        while not menu.Buttons.ReportPressed()[menu.ButtonEsc]:
            value = lcd._Contrast
            menu.Display.SetCursor(menu.Display.Width-len("%4d" % value),1)
            menu.Display.Print("%4d"% value)
	    
	    if menu.Buttons.ReportPressed()[menu.ButtonLeft]:
                print 'Left'
                value = lcd._Contrast - 1
		if value < 0 : value = 0              
		lcd.Contrast(value)
                print 'Value: ',value
                menu.Display.SetCursor(menu.Display.Width-len("%4d" % value),1)
                menu.Display.Print("%4d"% value)
            if menu.Buttons.ReportPressed()[menu.ButtonRight]:
                print 'Left'
                value = lcd._Contrast + 1
                if value > 255 : value = 255
                lcd.Contrast(value)
                print 'Value: ',value
                menu.Display.SetCursor(menu.Display.Width-len("%4d" % value),1)
                menu.Display.Print("%4d"% value)
            sleep(.2)

class BacklightMenu():
    ''' Should move to seperate file '''
    def __init__(self):
        pass

    @staticmethod
    def Show(menu):
        menu.Display.Print("Set Backlight")
        menu.Display.SetCursor(0,1)
        menu.Display.Print("Value:")
        menu.Display.Cursor(False,False)
        while not menu.Buttons.ReportPressed()[menu.ButtonEsc]:
            value = lcd._Backlight
            menu.Display.SetCursor(menu.Display.Width-len("%4d" % value),1)
            menu.Display.Print("%4d"% value)

            if menu.Buttons.ReportPressed()[menu.ButtonLeft]:
                print 'Left'
                value = lcd._Backlight - 1
                if value < 0 : value = 0
                lcd.Backlight(value)
                print 'Value: ',value
                menu.Display.SetCursor(menu.Display.Width-len("%4d" % value),1)
                menu.Display.Print("%4d"% value)
            if menu.Buttons.ReportPressed()[menu.ButtonRight]:
                print 'Left'
                value = lcd._Backlight + 1
                if value > 255 : value = 255
                lcd.Backlight(value)
                print 'Value: ',value
                menu.Display.SetCursor(menu.Display.Width-len("%4d" % value),1)
                menu.Display.Print("%4d"% value)
            sleep(.2)


class FrequencyMenu():
    ''' Should move to seperate file '''
    def __init__(self):
        pass

    @staticmethod
    def Show(menu):
        menu.Display.Print("Set frequency")
        menu.Display.SetCursor(0,1)
        menu.Display.Print("Value:")
        menu.Display.Cursor(False,False)
        while not menu.Buttons.ReportPressed()[menu.ButtonEsc]:
            value = lcd._Backlight
            menu.Display.SetCursor(menu.Display.Width-len("%4d" % value),1)
            menu.Display.Print("%4d"% value)

            if menu.Buttons.ReportPressed()[menu.ButtonLeft]:
                print 'Left'
                value = lcd._Backlight - 1
                if value < 0 : value = 0
                lcd.Backlight(value)
                print 'Value: ',value
                menu.Display.SetCursor(menu.Display.Width-len("%4d" % value),1)
                menu.Display.Print("%4d"% value)
            if menu.Buttons.ReportPressed()[menu.ButtonRight]:
                print 'Left'
                value = lcd._Backlight + 1
                if value > 255 : value = 255
                lcd.Backlight(value)
                print 'Value: ',value
                menu.Display.SetCursor(menu.Display.Width-len("%4d" % value),1)
                menu.Display.Print("%4d"% value)
            sleep(.2)



RPi_Ui_16x2.DefaultAddress = 148
lcd = RPi_Ui_16x2(I2C(1))
lcd.SetPinConfig(1,MCP9700)

lcd.Contrast(60)
lcd.Backlight(50)
lcd.Cls()

Submenu = Menu(lcd,[MenuItem(' Backlight', BacklightMenu()),
                    MenuItem(' Contrast', ContrastMenu())])

menu = Menu(lcd,[MenuItem(' Change Freq',FrequencyMenu()),
                 MenuItem(' En/Disable TX', Submenu),
                 MenuItem(' Image generator', Generator()),
                 MenuItem(' Settings',Submenu)])

menu.Show()
