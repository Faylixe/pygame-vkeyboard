#!/usr/bin/env python
# coding: utf8

"""
Module for keys definitions. It contains the following classes:

- `VKey`           : base class for all keys
- `VSpaceKey`      : *space* key definition
- `VBackKey`       : *delete* key definition

- `VActionKey`     : base class for key without effect on text
- `VUppercaseKey`  : *shift* key definition
- `VSpecialCharKey`: change the keyboard layout
"""

import pygame  # pylint: disable=import-error


class VKey(pygame.sprite.DirtySprite):
    """
    Simple key holder class.

    Holds key information (its value), as its state, size / position.
    State attributes with their default values:

    pressed = 0
        If set to 0, the key is released.
        If set to 1, the key is pressed.

    selected = 0
        If set to 0, the key is selectable but not selected.
        If set to 1, the key is selected.
    """

    def __init__(self, value, symbol=None):
        """Default key constructor.

        Parameters
        ----------
        value:
            Value of this key.
        symbol:
            Visual representation of the key displayed to the screen
            (equal to the value if not given).
        """
        super(VKey, self).__init__()
        self.pressed = 0
        self.selected = 0
        self.value = value
        self.symbol = symbol
        self.rect = pygame.Rect((0, 0), (10, 10))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        self.renderer = None
        self.pressed_key = None

    def __str__(self):
        """Key representation when using str() or print()"""
        if self.symbol:
            return self.symbol
        return self.value

    def set_position(self, x, y):
        """Set the key position.

        Parameters
        ----------
        x:
            Position x.
        y:
            Position y.
        """
        if self.rect.topleft != (x, y):
            self.rect.topleft = (x, y)
            self.dirty = 1

    def set_size(self, width, height):
        """Set the key size.

        Parameters
        ----------
        width:
            Background width.
        height:
            Background height.
        """
        if self.rect.size != (width, height):
            self.rect.size = (width, height)
            self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
            self.renderer.draw_key(self.image, self)
            self.dirty = 1

    def set_uppercase(self, uppercase):
        """Set key uppercase state and redraws it.

        Parameters
        ----------
        uppercase:
            True if uppercase, False otherwise.
        """
        if uppercase:
            new_value = self.value.upper()
        else:
            new_value = self.value.lower()
        if new_value != self.value:
            self.value = new_value
            self.renderer.draw_key(self.image, self)
            self.dirty = 1

    def set_pressed(self, state):
        """Set the key pressed state (1 for pressed 0 for released)
        and redraws it.

        Parameters
        ----------
        state:
            New key state.
        """
        if self.pressed != int(state):
            self.pressed = int(state)
            self.renderer.draw_key(self.image, self)
            self.dirty = 1

    def set_selected(self, state):
        """Set the key selection state (1 for selected else 0)
        and redraws it.

        Parameters
        ----------
        state:
            New key state.
        """
        if self.selected != int(state):
            self.selected = int(state)
            self.renderer.draw_key(self.image, self)
            self.dirty = 1

    def update(self, events):
        """Pygame events processing callback method.

        Parameters
        ----------
        events:
            List of events to process.
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN\
                    and event.button in (1, 2, 3):
                # Don't consider the mouse wheel (button 4 & 5):
                if self.rect.collidepoint(event.pos):
                    self.set_pressed(1)
            elif event.type == pygame.MOUSEBUTTONUP\
                    and event.button in (1, 2, 3):
                # Don't consider the mouse wheel (button 4 & 5):
                self.set_pressed(0)
            elif event.type == pygame.FINGERDOWN:
                display_size = pygame.display.get_surface().get_size()
                finger_pos = (event.x * display_size[0], event.y * display_size[1])
                if self.rect.collidepoint(finger_pos):
                    self.set_pressed(1)
            elif event.type == pygame.FINGERUP:
                self.set_pressed(0)
            elif event.type == pygame.KEYDOWN:
                if event.unicode and event.unicode == self.value:
                    self.set_pressed(1)
                    self.pressed_key = event.key
                elif event.key == self.value:
                    self.set_pressed(1)
                    self.pressed_key = event.key
                elif event.key == pygame.K_RETURN and self.selected:
                    self.set_pressed(1)
                    self.pressed_key = event.key
            elif event.type == pygame.KEYUP and self.pressed_key is not None:
                self.set_pressed(0)
                self.pressed_key = None
            elif event.type == pygame.JOYBUTTONDOWN and event.button == 0\
                    and self.selected:  # Select button pressed
                self.set_pressed(1)
            elif event.type == pygame.JOYBUTTONUP and event.button == 0\
                    and self.selected:  # Select button released
                self.set_pressed(0)

    def update_buffer(self, string):
        """Text update method.

        Aims to be called internally when a key collision has been detected.
        Updates and returns the given buffer using this key value.

        Parameters
        ----------
        string:
            Buffer to be updated.

        Returns
        -------
        string:
            Updated buffer value.
        """
        return string + self.value


class VSpaceKey(VKey):
    """Custom key for spacebar. """

    def __init__(self, length):
        """Default constructor.

        Parameters
        ----------
        length:
            Key length.
        """
        VKey.__init__(self, ' ', u'space')
        self.length = length

    def set_uppercase(self, uppercase):
        """Nothing to do on upper case action."""
        pass

    def set_size(self, width, height):
        """Sets the size of this key.

        Parameters
        ----------
        width:
            Background width.
        height:
            Background height.
        """
        super(VSpaceKey, self).set_size(width * self.length, height)


class VBackKey(VKey):
    """Custom key for back. """

    def __init__(self):
        """Default constructor. """
        VKey.__init__(self, u'\x7f', u'\u2190')

    def set_uppercase(self, uppercase):
        """Nothing to do on upper case action."""
        pass

    def update_buffer(self, string):
        """Text update method. Removes last character.

        Parameters
        ----------
        string:
            Buffer to be updated.

        Returns
        -------
        string:
            Updated buffer value.
        """
        return string[:-1]


class VActionKey(VKey):
    """
    A VActionKey is a key that trigger an action
    rather than updating the buffer when pressed.
    """

    def __init__(self, action, state_holder, symbol, activated_symbol):
        """Default constructor.

        Parameters
        ----------
        action:
            Delegate action called when this key is pressed.
        state_holder:
            Holder for this key state (activated or not).
        """
        super(VActionKey, self).__init__('', symbol)
        self.action = action
        self.state_holder = state_holder
        self.activated_symbol = activated_symbol
        self.activated = False

    def __str__(self):
        """Key representation when using str() or print()"""
        if self.is_activated():
            self.activated = True
            return self.activated_symbol
        return self.symbol

    def update(self, events):
        """Check if state holder has changed."""
        super(VActionKey, self).update(events)
        if self.activated != self.is_activated() and not self.dirty:
            self.activated = self.is_activated()
            self.renderer.draw_key(self.image, self)
            self.dirty = 1

    def set_uppercase(self, uppercase):
        """Nothing to do on upper case action."""
        pass

    def set_pressed(self, state):
        """Nothing to do on upper case action."""
        prev_state = self.pressed
        super(VActionKey, self).set_pressed(state)
        if prev_state != self.pressed and self.pressed == 0:
            # The key is getting unpressed
            self.action()

    def is_activated(self):
        """Indicates if this key is activated.

        Returns
        -------
        is_activated: bool
            True if activated, False otherwise.
        """
        raise NotImplementedError(
            "Method 'is_activated' have to be overwritten")

    def update_buffer(self, string):
        """Do not update text but trigger the delegate action.

        Parameters
        ----------
        string:
            Not used, just to match parent interface.

        Returns
        -------
        string:
            Buffer provided as parameter.
        """
        return string


class VUppercaseKey(VActionKey):
    """Action key for the uppercase switch. """

    def __init__(self, action, state_holder):
        super(VUppercaseKey, self).__init__(action,
                                            state_holder,
                                            u'\u21e7',
                                            u'\u21ea')
        self.value = pygame.K_LSHIFT

    def is_activated(self):
        """Indicates if this key is activated.

        Returns
        -------
        is_activated: bool
            True if activated, False otherwise.
        """
        return self.state_holder.uppercase


class VSpecialCharKey(VActionKey):
    """Action key for the special char switch. """

    def __init__(self, action, state_holder):
        super(VSpecialCharKey, self).__init__(action,
                                              state_holder,
                                              u'#',
                                              u'Ab')

    def is_activated(self):
        """Indicates if this key is activated.

        Returns
        -------
        is_activated: bool
            True if activated, False otherwise.
        """
        return self.state_holder.special_char
