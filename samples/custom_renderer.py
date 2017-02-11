#!/usr/bin/python

""" Simple keyboard usage using AZERTY layout. """

import pygame
from pygame.locals import *
from pygame_vkeyboard import *

def consumer(text):
    """ Simple text consumer. """
    print('Current text state: %s' % text)

WHITE = (255, 255, 255)
BACKGROUND = (0, 0, 0, 150)
FONT = pygame.font.SysFont('arial', 40)

class TransparentRenderer(object):
    """
    """
        
    def draw_background(self, surface, position, size):
        """Default drawing method for background.

        Background is drawn as a simple rectangle filled using this
        style background color attribute.

        :param surface: Surface background should be drawn in.
        :param position: Surface relative position the keyboard should be drawn at.
        :param size: Expected size of the drawn keyboard.
        """
        pygame.draw.rect(surface, BACKGROUND, position + size)
    
    def draw_key(self, surface, key):
        """Default drawing method for key. 

        Key is drawn as a simple rectangle filled using this
        cell style background color attribute. Key value is printed
        into drawn cell using internal font.

        :param surface: Surface background should be drawn in.
        :param key: Target key to be drawn.
        """
        pygame.draw.rect(surface, WHITE, key.position + (key.size, key.size), 1)
        return surface.blit(FONT.render(key.value, 1, WHITE, None), key.position)

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
            