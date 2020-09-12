#!/usr/bin/env python
# coding: utf8

"""Simple keyboard usage using custom numeric layout."""

# pylint: disable=import-error
import pygame
import pygame_vkeyboard as vkboard
# pylint: enable=import-error


def on_key_event(text):
    """ Print the current text. """
    print('Current text:', text)


def main(test=False):
    """ Main program.

    :param test: Indicate function is being tested
    :type test: bool
    :return: None
    """

    # Init pygame
    pygame.init()
    screen = pygame.display.set_mode((400, 400))

    # Create keyboard
    model = ['123', '456', '789', '*0#']
    layout = vkboard.VKeyboardLayout(model,
                                     key_size=30,
                                     padding = 15,
                                     height_ratio=0.8,
                                     allow_uppercase=False,
                                     allow_special_chars=False,
                                     allow_space=False)
    keyboard = vkboard.VKeyboard(screen, on_key_event, layout,
                                 joystick_navigation=True)

    # Main loop
    while True:

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                exit()

        keyboard.update(events)
        rects = keyboard.draw(screen)

        # Flip only the updated area
        pygame.display.update(rects)

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()
