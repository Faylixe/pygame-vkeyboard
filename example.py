#!/usr/bin/python

import pygame
from pygame.locals import *

from vkeyboard import VKeyboard

def consumer(text):
    """ Simple text consumer. """
    print('Current text : %s' % text)

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    window = pygame.display.set_mode((600, 400))
    keyboard = VKeyboard(window, consumer)
    keyboard.active = True
    keyboard.draw()
    running = True
    while running:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                # TODO : press
            elif event.type == MOUSEBUTTONUP:
                # TODO : release