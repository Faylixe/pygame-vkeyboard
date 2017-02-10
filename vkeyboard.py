#!/usr/bin/python

import pygame
from pygame.locals import *

pygame.font.init()

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
    """
    """

    def __init__(self, value):
        """ """
        self.state = 0
        self.value = value
        self.start = -1
        self.width = 0

    def isTouched(self, position):
        """ """
        return position[0] >= self.start and position[0] <= self.start + self.width
    
    def updateBuffer(self, buffer):
        """ """
        return buffer + self.value

class VKeyRow(object):
    """ """

    def __init__(self):
        """ """
        self.keys = []
        self.start = -1
        self.height = 0

    def setSize(self, size, padding):
        """ """
        self.height = size
        i = padding
        for key in self.keys:
            key.width = size
            key.start = i
            i += padding + size

    def __contains__(self, position):
        """ """
        return position[1] >= self.start and position[1] <= self.start + self.height

    def __len__(self):
        return len(self.keys)

class VKeyboardLayout(object):
    """ Keyboard layout class. """

    # Default AZERTY layout.
    AZERTY = ['azertyuiop', 'qsdfghjklm', 'wxcvbn']
    
    def __init__(self, model, allowUpperCase, allowSpecialChars):
        """ Default constructor. Initializes layout rows. """
        self.keyrows = []
        i = 0
        for row in model:
            keyrow = VKeyRow()
            if i == 0: keyrow.keys.append(VKey('<-')) # Back key.
            elif i == 1 and allowUpperCase: keyrow.keys.append(VKey('MAJ')) # Majlock.
            elif i == 2 and allowSpecialChars: keyrow.keys.append(VKey('123')) # Special chars.
            for value in row:
                keyrow.keys.append(VKey(value))
            self.keyrows.append(keyrow)
            i += 1

    def computeBound(self, surfaceSize, padding):
        """ Compute keyboard bound. """
        maxLength = len(max(self.keyrows, key=len))
        self.cellSize = (surfaceSize[0] - (padding * (maxLength + 1))) / maxLength
        height = self.cellSize * len(self.keyrows) + padding * (len(self.keyrows) + 1)
        self.size = (surfaceSize[0], height)
        self.position = (0, surfaceSize[1] - self.size[1])
        i = self.position[1] + padding
        for row in self.keyrows:
            row.start = i
            row.setSize(self.cellSize, padding)
            i += padding + self.cellSize
        return self.cellSize

    def getKeyAt(self, position):
        """ """
        for keyrow in self.keyrows:
            if position in keyrow:
                for key in keyrow.keys:
                    if key.isTouched(position):
                        return key
        return None

class VKeyboard(object):
    """ Virtual Keyboard class. """

    def __init__(
        self,
        window,
        textConsumer,   
        layout,
        style=VKeyboardStyle.DEFAULT,
        allowSpecialChars=True,
        allowUpperCase=True):
        """ Default constructor. """
        self.window = window
        self.textConsumer = textConsumer
        self.layout = layout
        self.style = style
        self.buffer = ''
        self.state = 0
        bound = layout.computeBound(window.get_size(), style.padding)
        self.cellSize = (bound, bound)

    def enable(self):
        """ """
        self.state = 1

    def draw(self):
        """ Draw the virtual keyboard into the delegate window object. """
        if self.state > 0:
            self.style.drawBackground(self.window, self.layout.position, self.layout.size)
            padding = self.style.padding
            y = self.layout.position[1] + padding
            for row in self.layout.keyrows:
                x = padding
                for key in row.keys:
                    self.style.drawKey(self.window, key.value, (x, y), self.cellSize)
                    x += self.cellSize[0] + padding
                y += self.cellSize[0] + padding

    def onKeyDown(self, position):
        """ """
        if self.state > 0:
            key = self.layout.getKeyAt(position)
            if key is not None:
                key.state = 1

    def onKeyUp(self, position):
        """ """
        if self.state > 0:
            key = self.layout.getKeyAt(position)
            if key is not None:
                key.state = 0
                self.buffer = key.updateBuffer(self.buffer)
                self.textConsumer(self.buffer)
            
