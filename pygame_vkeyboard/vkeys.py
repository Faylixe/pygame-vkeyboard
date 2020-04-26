#!/usr/bin/env python
# coding: utf8

"""
    TODO: Document.
"""

import pygame  # pylint: disable=import-error


class VKey(pygame.sprite.DirtySprite):
    """
    Simple key holder class.

    Holds key information (its value), as it's state, 1 for pressed,
    0 for released. Also contains it size / position properties.
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
        self.state = 0
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
        """Set the key state (1 for pressed 0 for released)
        and redraws it.

        Parameters
        ----------
        state:
            New key state.
        """
        if self.state != int(state):
            self.state = int(state)
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.set_pressed(1)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.set_pressed(0)
            if event.type == pygame.KEYDOWN:
                if event.unicode and event.unicode == self.value:
                    self.set_pressed(1)
                    self.pressed_key = event.key
                elif event.key == self.value:
                    self.set_pressed(1)
                    self.pressed_key = event.key
            elif event.type == pygame.KEYUP and self.pressed_key is not None:
                self.set_pressed(0)
                self.pressed_key = None

    def update_buffer(self, buffer):
        """Text update method.

        Aims to be called internally when a key collision has been detected.
        Updates and returns the given buffer using this key value.

        Parameters
        ----------
        buffer:
            Buffer to be updated.

        Returns
        -------
        buffer:
            Updated buffer value.
        """
        return buffer + self.value


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

    def set_size(self,  width, height):
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

    def update_buffer(self, buffer):
        """Text update method. Removes last character.

        Parameters
        ----------
        buffer:
            Buffer to be updated.

        Returns
        -------
        buffer:
            Updated buffer value.
        """
        return buffer[:-1]


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
        prev_state = self.state
        super(VActionKey, self).set_pressed(state)
        if prev_state != self.state and self.state == 0:
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

    def update_buffer(self, buffer):
        """Do not update text but trigger the delegate action.

        Parameters
        ----------
        buffer:
            Not used, just to match parent interface.

        Returns
        -------
        buffer:
            Buffer provided as parameter.
        """
        return buffer


class VUppercaseKey(VActionKey):
    """Action key for the uppercase switch. """

    def __init__(self, action, state_holder):
        super(VUppercaseKey, self).__init__(
            action,
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
        super(VSpecialCharKey, self).__init__(
            action,
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
