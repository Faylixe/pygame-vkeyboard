#!/usr/bin/python

""" Simple keyboard usage using custom numeric layout. """

import pygame
from pygame.locals import *
from pygame_vkeyboard import *

def consumer(text):
    """ Simple text consumer. """
    print(repr('Current text state: %s' % text))

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((600, 400))
    model = ['123', '456', '789', '0']
    layout = VKeyboardLayout(model, allow_uppercase=False, allow_special_chars=False, allow_space=False)
    keyboard = VKeyboard(window, consumer, layout)
    keyboard.enable()
    running = True
    while running:
        pygame.display.flip()
        for event in pygame.event.get():
            keyboard.on_event(event)
            if event.type == QUIT:
                running = False
            