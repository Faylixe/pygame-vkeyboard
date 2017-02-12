#!/usr/bin/python

""" Simple keyboard usage using AZERTY layout. """

import pygame
from pygame.locals import *
from pygame_vkeyboard import *

def consumer(text):
    print(repr('Current text state: %s' % text))

WHITE = (255, 255, 255)
BACKGROUND = (0, 0, 0, 150)
FONT = pygame.font.SysFont('arial', 40)


class TransparentRenderer(VKeyboardRenderer):

    def draw_background(self, surface, position, size):
        pygame.draw.rect(surface, (0, 0, 0, 150), position + size)
    
    def draw_character_key(self, surface, key, special=False):
        pygame.draw.rect(surface, WHITE, key.position + (key.size, key.size), 1)
        surface.blit(FONT.render(key.value, 1, WHITE, None), key.position)

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((600, 400))
    layout = VKeyboardLayout(VKeyboardLayout.AZERTY)
    keyboard = VKeyboard(window, consumer, layout, renderer=TransparentRenderer())
    keyboard.enable()
    keyboard.draw()
    running = True
    while running:
        pygame.display.flip()
        for event in pygame.event.get():
            keyboard.on_event(event)
            if event.type == QUIT:
                running = False
            