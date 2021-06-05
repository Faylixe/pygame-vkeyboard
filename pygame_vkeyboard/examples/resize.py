#!/usr/bin/env python
# coding: utf8

"""Simple keyboard usage using QWERTY layout and input text."""

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
    screen = pygame.display.set_mode((500, 300), pygame.RESIZABLE)
    screen.fill((100, 100, 100))

    # Create keyboard
    layout = vkboard.VKeyboardLayout(vkboard.VKeyboardLayout.QWERTY,
                                     allow_special_chars=False,
                                     allow_space=False)
    keyboard = vkboard.VKeyboard(screen,
                                 on_key_event,
                                 layout,
                                 renderer=vkboard.VKeyboardRenderer.DARK,
                                 show_text=True,
                                 joystick_navigation=True)

    clock = pygame.time.Clock()

    # Main loop
    while True:
        clock.tick(100)  # Ensure not exceed 100 FPS

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                print("Average FPS: ", clock.get_fps())
                exit()
            if event.type == pygame.VIDEORESIZE:
                screen.fill((100, 100, 100))

        keyboard.update(events)
        rects = keyboard.draw(screen)

        # Flip only the updated area
        pygame.display.update(rects)

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()
