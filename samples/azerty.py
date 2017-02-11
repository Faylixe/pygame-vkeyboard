#!/usr/bin/python

""" Simple keyboard usage using AZERTY layout. """

import pygame
from pygame.locals import *
from pygame_vkeyboard import *

def consumer(text):
    """ Simple text consumer. """
    print('Current text state: %s' % text)

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((600, 400))
    layout = VKeyboardLayout(VKeyboardLayout.AZERTY)
    keyboard = VKeyboard(window, consumer, layout)
    keyboard.enable()
    keyboard.draw()
    running = True
    while running:
        pygame.display.flip()
        for event in pygame.event.get():
            keyboard.on_event(event)
            if event.type == QUIT:
                running = False
            