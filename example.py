#!/usr/bin/python

import pygame
from pygame.locals import *

from vkeyboard import VKeyboard, VKeyboardLayout

def consumer(text):
    """ Simple text consumer. """
    print('Current text : %s' % text)

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    window = pygame.display.set_mode((600, 400))
    layout = VKeyboardLayout(VKeyboardLayout.AZERTY)
    keyboard = VKeyboard(window, consumer, layout)
    keyboard.enable()
    keyboard.draw()
    running = True
    while running:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                keyboard.on_key_down(pygame.mouse.get_pos())
            elif event.type == MOUSEBUTTONUP:
                keyboard.on_key_up(pygame.mouse.get_pos())