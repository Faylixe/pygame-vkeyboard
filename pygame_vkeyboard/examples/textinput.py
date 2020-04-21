#!/usr/bin/env python
# coding: utf8

""" Simple keyboard usage using AZERTY layout. """

import pygame  # pylint: disable=import-error
import pygame_vkeyboard as vkboard


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
    screen = pygame.display.set_mode((300, 400))
    screen.fill((200, 200, 200))

    # Create keyboard
    layout = vkboard.VKeyboardLayout(vkboard.VKeyboardLayout.QWERTY)
    keyboard = vkboard.VKeyboard(screen, on_key_event, layout, show_text_input=True)
    keyboard.enable()

    clock = pygame.time.Clock()

    # Main loop
    while True:
        clock.tick(100)

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                print("Average FPS: ", clock.get_fps())
                exit()

        keyboard.update(events)

        keyboard.draw()

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()
