#!/usr/bin/python

import pygame
from pygame.locals import *

pygame.font.init()

class VKeyboardLayout(object):
    """ Keyboard layout class. """

    def __init__(self, rows):
        """ Default constructor. """
        self.rows = rows

# Default AZERTY layout.
VKeyboardLayout.AZERTY = VKeyboardLayout(['azertyuiop', 'qsdfghjklm', 'wxcvbn'])

class VKeyboardStyle(object):
    """ """

    def __init__(
        self,
        font,
        keyboardBackgroundColor,
        cellBackgroundColor,
        textColor,
        padding):
        """ Default constructor. """
        self.font = pygame.font.SysFont('arial', 20)
        self.keyboardBackgroundColor = keyboardBackgroundColor
        self.cellBackgroundColor = cellBackgroundColor
        self.textColor = textColor
        self.padding = padding
        
    def drawBackground(self, surface, position, size):
        """ Default drawing method for background. """
        pygame.draw.rect(surface, self.keyboardBackgroundColor, position + size)
    
    def drawKey(self, surface, key, position, size):
        """ Default drawing method for key. """
        pygame.draw.rect(surface, self.cellBackgroundColor, position + size)
        return surface.blit(self.font.render(key, 1, self.textColor, None), position) # TODO : Center key.

# Default style.
VKeyboardStyle.DEFAULT = VKeyboardStyle(
    pygame.font.SysFont('arial', 20),
    (50, 50, 50),
    (255, 255, 255),
    (0, 0, 0),
    5
)

class VKey(object):
    """ """

    def __init__(self, value):
        """ """
        self.state = 0
        self.value = value
        self.position = None

    def isTouched(self, position):
        """ """
        return False
    
    def updateBuffer(self, buffer):
        """ """
        buffer += self.value

class VKeyRow(object):
    """ """

    def __init__(self):
        """ """
        self.keys = []

    def __contains__(self, position):
        """ """
        return False

class VKeyboard(object):
    """ Virtual Keyboard class. """

    def __init__(
        self,
        window,
        textConsumer,
        layout=VKeyboardLayout.AZERTY,
        style=VKeyboardStyle.DEFAULT):
        """ Default constructor. """
        self.window = window
        self.textConsumer = textConsumer
        self.layout = layout
        self.style = style
        self.buffer = ''
        self.active = False
        self.special = False
        self.computeKeyboardBound() 
        self.rows = []

    def computeKeyboardBound(self):
        """ Compute keyboard bound. """
        padding = self.style.padding
        surfaceSize = self.window.get_size()
        maxLength = len(max(self.layout.rows, key=len))
        cellSize = (surfaceSize[0] - (padding * (maxLength + 1))) / maxLength
        self.cellSize = (cellSize, cellSize)
        height = cellSize * len(self.layout.rows) + padding * (len(self.layout.rows) + 1)
        self.size = (surfaceSize[0], height)
        self.position = (0, surfaceSize[1] - self.size[1])

    def draw(self):
        """ Draw the virtual keyboard into the delegate window object. """
        if self.active:
            self.style.drawBackground(self.window, self.position, self.size)
            padding = self.style.padding
            y = self.position[1] + padding
            for row in self.layout.rows:
                x = padding
                for key in row:
                    self.style.drawKey(self.window, key, (x, y), self.cellSize)
                    x += self.cellSize[0] + padding
                y += self.cellSize[0] + padding

    def getKey(self, position):
        """ """
        for row in self.rows :
            if position in row:
                for key in row:
                    if key.isTouched(position):
                        return key
        return None

    def onKeyDown(self, position):
        """ """
        key = self.getKey(position)
        if key is not None:
            key.state = 1

    def onKeyUp(self, position):
        """ """
         key = self.getKey(position)
         if key is not None:
            key.state = 0
            key.updateBuffer(self.buffer)
            
