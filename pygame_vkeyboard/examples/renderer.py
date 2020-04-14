#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Simple keyboard usage using AZERTY layout."""

import pygame
import pygame_vkeyboard as vkboard


WHITE = (255, 255, 255)
BACKGROUND = (0, 0, 0, 150)
FONT = pygame.font.SysFont('arial', 40)


def on_key_event(text):
    """
    Print the current text.
    """
    print('Current text:', text)


class TransparentRenderer(vkboard.VKeyboardRenderer):

    def draw_background(self, surface, position, size):
        pygame.draw.rect(surface, (0, 0, 0, 150), position + size)

    def draw_character_key(self, surface, key, special=False):
        pygame.draw.rect(surface, WHITE, key.position + (key.size, key.size), 1)
        surface.blit(FONT.render(key.value, 1, WHITE, None), key.position)


def main(test=False):
    """
    Main program.

    :param test: Indicate function is being tested
    :type test: bool
    :return: None
    """

    # Init pygame
    pygame.init()
    screen = pygame.display.set_mode((600, 400))

    # Create keyboard
    layout = vkboard.VKeyboardLayout(vkboard.VKeyboardLayout.AZERTY)
    keyboard = vkboard.VKeyboard(screen, on_key_event, layout, renderer=TransparentRenderer())
    keyboard.enable()
    keyboard.draw()

    # Main loop
    while True:

        for event in pygame.event.get():
            keyboard.on_event(event)
            if event.type == pygame.QUIT:
                exit()

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break

if __name__ == '__main__':
    main()
