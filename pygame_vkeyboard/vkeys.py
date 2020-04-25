# coding: utf8


import pygame  # pylint: disable=import-error


class VKey(object):
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
        self.state = 0
        self.value = value
        self.symbol = symbol
        self.position = (0, 0)
        self.size = (0, 0)

    def __eq__(self, other):
        """Return True if self equal other"""
        if isinstance(other, VKey):
            return self.value == other.value
        return self.value == other

    def __str__(self):
        """Key representation when using str() or print()"""
        if self.symbol:
            return self.symbol
        return self.value

    def set_size(self, size):
        """Sets the size of this key.

        Parameters
        ----------
        size:
            Size of this key.
        """
        self.size = (size, size)

    def is_touched(self, position):
        """Hit detection method.

        Indicates if this key has been hit by a touch / click event at the
        given position.

        Parameters
        ----------
        position:
            Event position.

        Returns
        -------
        is_touched:
            True is the given position collide this key, False otherwise.
        """
        return all((position[0] >= self.position[0],
                    position[0] <= self.position[0] + self.size[0]))

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

    def set_size(self, size):
        """Sets the size of this key.

        Parameters
        ----------
        size:
            Size of this key.
        """
        self.size = (size * self.length, size)


class VBackKey(VKey):
    """Custom key for back. """

    def __init__(self):
        """Default constructor. """
        VKey.__init__(self, u'\x7f', u'\u2190')

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
        VKey.__init__(self, '', symbol)
        self.action = action
        self.state_holder = state_holder
        self.activated_symbol = activated_symbol

    def __str__(self):
        """Key representation when using str() or print()"""
        if self.is_activated():
            return self.activated_symbol
        return self.symbol

    def is_activated(self):
        """Indicates if this key is activated.

        Returns
        -------
        is_activated: bool
            True if activated, False otherwise.
        """
        raise NotImplementedError("Method 'is_activated' have to be overwritten")

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
        self.action()
        return buffer


class VUppercaseKey(VActionKey):
    """Action key for the uppercase switch. """

    def __init__(self, action, state_holder):
        super(VUppercaseKey, self).__init__(action, state_holder, u'\u21e7', u'\u21ea')
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
        super(VSpecialCharKey, self).__init__(action, state_holder, u'#', u'Ab')

    def is_activated(self):
        """Indicates if this key is activated.

        Returns
        -------
        is_activated: bool
            True if activated, False otherwise.
        """
        return self.state_holder.special_char
