#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Simple keyboard usage using custom numeric layout."""

import pygame
import pygame_vkeyboard as vkboard


def on_key_event(text):
    """
    Print the current text.
    """
    print('Current text:', text)


def main(test=False):
    """
    Main program.

    :param test: Indicate function is being tested
    :type test: bool
    :return: None
    """

    # Init pygame
    pygame.init()
    screen = pygame.display.set_mode((300, 400))

    # Create keyboard
    model = ['123', '456', '789', '*0#']
    layout = vkboard.VKeyboardLayout(model, key_size=40, allow_uppercase=False,
                                     allow_special_chars=False, allow_space=False)
    keyboard = vkboard.VKeyboard(screen, on_key_event, layout)
    keyboard.enable()

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
