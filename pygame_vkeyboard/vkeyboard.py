#!/usr/bin/env python
# coding: utf8

"""
    Visual keyboard for Pygame engine. Aims to be easy to use
    as highly customizable as well.

    ``VKeyboard`` only require a pygame surface to be displayed
    on and a text consumer function, as in the following example :

    ```python
    from pygame_vkeyboard import *

    # Initializes your window object or surface your want
    # vkeyboard to be displayed on top of.
    surface = ...

    def consume(text):
        print(repr('Current text : %s' % text))

    # Initializes and activates vkeyboard
    layout = VKeyboardLayout(VKeyboardLayout.AZERTY)
    keyboard = VKeyboard(window, consumer, layout)
    keyboard.enable()
    ```
"""

import logging
import pygame  # pylint: disable=import-error

from os.path import join, dirname

# Configure logger.
logging.basicConfig()
logger = logging.getLogger(__name__)


class VKeyboardRenderer(object):
    """
        A VKeyboardRenderer is in charge of keyboard rendering.

        It handles keyboard rendering properties such as color or padding,
        and provides two types of rendering methods : one for the keyboard
        background and another one the the key rendering.

        .. note::
            A DEFAULT style instance is available as class attribute.
    """

    def __init__(
            self,
            font,
            keyboard_background_color,
            key_background_color,
            text_color,
            special_key_background_color=None):
        """ VKeyboardStyle default constructor.

        Parameters
        ----------
        font:
            Used font for rendering key.
        keyboard_background_color:
            Background color use for the keyboard.
        key_background_color:
            Tuple of background color for key (one value per state).
        text_color:
            Tuple of key text color (one value per state).
        special_key_background_color:
            Background color for special key if required.
        """
        self.font = font
        self.keyboard_background_color = keyboard_background_color
        self.key_background_color = key_background_color
        self.special_key_background_color = special_key_background_color
        self.text_color = text_color

    def draw_background(self, surface, position, size):
        """ Default drawing method for background.

        Background is drawn as a simple rectangle filled using this
        style background color attribute.

        Parameters
        ----------
        surface:
            Surface background should be drawn in.
        position:
            Surface relative position the keyboard should be drawn at.
        size:
            Expected size of the drawn keyboard.
        """
        pygame.draw.rect(
            surface,
            self.keyboard_background_color,
            position + size)

    def draw_key(self, surface, key):
        """ Default drawing method for key.

        Draw the key accordingly to it type.

        Parameters
        ----------
        surface:
            Surface background should be drawn in.
        key:
            Target key to be drawn.
        """
        if isinstance(key, VSpaceKey):
            self.draw_space_key(surface, key)
        elif isinstance(key, VBackKey):
            self.draw_back_key(surface, key)
        elif isinstance(key, VUppercaseKey):
            self.draw_uppercase_key(surface, key)
        elif isinstance(key, VSpecialCharKey):
            self.draw_special_char_key(surface, key)
        else:
            self.draw_character_key(surface, key)

    def draw_character_key(self, surface, key, special=False):
        """ Default drawing method for key.

        Key is drawn as a simple rectangle filled using this
        cell style background color attribute. Key value is printed
        into drawn cell using internal font.

        Parameters
        ----------
        surface:
            Surface background should be drawn in.
        key:
            Target key to be drawn.
        special:
            Boolean flag that indicates if the drawn key should use
            special background color if available.
        """
        background_color = self.key_background_color
        if special and self.special_key_background_color is not None:
            background_color = self.special_key_background_color
        pygame.draw.rect(
            surface,
            background_color[key.state],
            key.position + key.size)
        size = self.font.size(key.value)
        x = key.position[0] + ((key.size[0] - size[0]) / 2)
        y = key.position[1] + ((key.size[1] - size[1]) / 2)
        surface.blit(
            self.font.render(
                key.value,
                1,
                self.text_color[key.state],
                None), (x, y))

    def draw_space_key(self, surface, key):
        """ Default drawing method space key.

        Key is drawn as a simple rectangle filled using this
        cell style background color attribute. Key value is printed
        into drawn cell using internal font.

        Parameters
        ----------
        surface:
            Surface background should be drawn in.
        key:
            Target key to be drawn.
        """
        self.draw_character_key(surface, key, False)

    def draw_back_key(self, surface, key):
        """ Default drawing method for back key. Drawn as character key.

        Parameters
        ----------
        surface:
            Surface background should be drawn in.
        key:
            Target key to be drawn.
        """
        self.draw_character_key(surface, key, True)

    def draw_uppercase_key(self, surface, key):
        """ Default drawing method for uppercase key. Drawn as character key.

        Parameters
        ----------
        surface:
            Surface background should be drawn in.
        key:
            Target key to be drawn.
        """
        key.value = u'\u21e7'
        if key.is_activated():
            key.value = u'\u21ea'
        self.draw_character_key(surface, key, True)

    def draw_special_char_key(self, surface, key):
        """ Default drawing method for special char key.
        Drawn as character key.

        Parameters
        ----------
        surface:
            Surface background should be drawn in.
        key:
            Target key to be drawn.
        """
        key.value = u'#'
        if key.is_activated():
            key.value = u'Ab'
        self.draw_character_key(surface, key, True)


pygame.font.init()
VKeyboardRenderer.DEFAULT = VKeyboardRenderer(
    pygame.font.Font(join(dirname(__file__), 'DejaVuSans.ttf'), 25),
    (255, 255, 255),
    ((255, 255, 255), (0, 0, 0)),
    ((0, 0, 0), (255, 255, 255)),
    ((180, 180, 180), (0, 0, 0)))
""" Default style implementation. """


class VKey(object):
    """
        Simple key holder class.

        Holds key information (its value), as it's state, 1 for pressed,
        0 for released. Also contains it size / position properties.
    """

    def __init__(self, value):
        """ Default key constructor.

        Parameters
        ----------
        value:
            Value of this key which also is the label displayed to the screen.
        """
        self.state = 0
        self.value = value
        self.position = (0, 0)
        self.size = (0, 0)

    def set_size(self, size):
        """ Sets the size of this key.

        Parameters
        ----------
        size:
            Size of this key.
        """
        self.size = (size, size)

    def is_touched(self, position):
        """ Hit detection method.

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
        """ Text update method.

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
    """ Custom key for spacebar. """

    def __init__(self, length):
        """ Default constructor.

        Parameters
        ----------
        length:
            Key length.
        """
        VKey.__init__(self, 'Space')
        self.length = length

    def set_size(self, size):
        """ Sets the size of this key.

        Parameters
        ----------
        size:
            Size of this key.
        """
        self.size = (size * self.length, size)

    def update_buffer(self, buffer):
        """ Text update method. Adds space to the given buffer.

        Parameters
        ----------
        buffer:
            Buffer to be updated.

        Returns
        -------
        buffer:
            Updated buffer value.
        """
        return buffer + ' '


class VBackKey(VKey):
    """ Custom key for back. """

    def __init__(self):
        """ Default constructor. """
        VKey.__init__(self, u'\u21a9')

    def update_buffer(self, buffer):
        """ Text update method. Removes last character.

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
        A VActionKey is a key that trigger and action
        rather than updating the buffer when pressed.
    """

    def __init__(self, action, state_holder):
        """ Default constructor.

        Parameters
        ----------
        action:
            Delegate action called when this key is pressed.
        state_holder:
            Holder for this key state (activated or not).
        """
        VKey.__init__(self, '')
        self.action = action
        self.state_holder = state_holder

    def update_buffer(self, buffer):
        """ Do not update text but trigger the delegate action.

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
    """ Action key for the uppercase switch. """

    def __init__(self, keyboard):
        """ Default constructor.

        Parameters
        ----------
        keyboard:
            Keyboard to trigger on_uppercase() when pressed.
        """
        VActionKey.__init__(self, lambda: keyboard.on_uppercase(), keyboard)

    def is_activated(self):
        """ Indicates if this key is activated.

        Returns
        -------
        is_activated: bool
            True if activated, False otherwise.
        """
        return self.state_holder.uppercase


class VSpecialCharKey(VActionKey):
    """ Action key for the special char switch. """

    def __init__(self, keyboard):
        """ Default constructor.

        Parameters
        ----------
        keyboard:
            Keyboard to trigger on_special_char() when pressed.
        """
        VActionKey.__init__(self, lambda: keyboard.on_special_char(), keyboard)

    def is_activated(self):
        """ Indicates if this key is activated.

        Returns
        -------
        is_activated: bool
            True if activated, False otherwise.
        """
        return self.state_holder.special_char


class VKeyRow(object):
    """
        A VKeyRow defines a keyboard row which is composed of a list of VKey.

        This class aims to be created internally after parsing a keyboard
        layout model. It is used to optimize collision detection, by first
        checking row collision, then internal row key detection.
    """

    def __init__(self):
        """ Default row constructor. """
        self.keys = []
        self.y = -1
        self.height = 0
        self.space = None

    def add_key(self, key, first=False):
        """ Adds the given key to this row.

        Parameters
        ----------
        key:
            Key to be added to this row.
        first:
            Flag that indicates if key is added at the beginning or at the end.
        """
        if first:
            self.keys = [key] + self.keys
        else:
            self.keys.append(key)
        if isinstance(key, VSpaceKey):
            self.space = key

    def set_size(self, position, size, padding):
        """ Row size setter. The size correspond to the row height, since the
        row width is constraint to the surface width the associated keyboard
        belongs. Once size is settled, the size for each child keys is
        associated.

        Parameters
        ----------
        position:
            Position of this row.
        size:
            Size of the row (height)
        padding:
            Padding between key.
        """
        self.height = size
        self.position = position
        x = position[0]
        for key in self.keys:
            key.set_size(size)
            key.position = (x, position[1])
            x += padding + key.size[0]

    def __contains__(self, position):
        """ Indicates if the given position collide this row.

        Parameters
        ----------
        position:
        Position to check againt this row.

        Returns
        -------
        contains:
            True if the given position collide this row, False otherwise.
        """
        return all((position[1] >= self.position[1],
                    position[1] <= self.position[1] + self.height))

    def __len__(self):
        """ len() operator overload.

        Returns
        -------
        len:
            Number of keys thi row contains.
        """
        return len(self.keys)


class VKeyboardLayout(object):
    """Keyboard layout class.

    A keyboard layout is built using layout model which consists in an
    list of supported character. Such list item as simple string containing
    characters assigned to a row.

    An erasing key is inserted automatically to the first row.

    If `allow_uppercase` flag is `True`, then an upper case key will be
    inserted at the beginning of the second row.

    If `allow_special_chars` flag is `True`, then an special
    characters / number key will be inserted at the beginning of the third row.
    Pressing this key will switch the associated keyboard current layout.
    """

    AZERTY = ['1234567890', 'azertyuiop', 'qsdfghjklm', 'wxcvbn']
    """ AZERTY Layout. """

    QWERTY = ['1234567890', 'qwertyuiop', 'asdfghjkl', 'wzxcvbnm']
    """ QWERTY Layout. """

    NUMBER = ['123', '456', '789', '0']
    """ Number only layout. """

    # TODO : Insert special characters layout which include number.
    SPECIAL = [u'&é"\'(§è!çà)', u'°_-^$¨*ù`%£', u',;:=?.@+<>#', u'[]{}/\\|']
    """ Special characters layout. """

    def __init__(
            self,
            model,
            key_size=None,
            padding=5,
            allow_uppercase=True,
            allow_special_chars=True,
            allow_space=True):
        """ Default constructor. Initializes layout rows.

        Parameters
        ----------
        model:
            Layout model to use.
        key_size:
            Size of the key, if not specified will be computed dynamically.
        padding:
            Padding between key (work horizontally as vertically).
        allowUpperCase:
            Boolean flag that indicates usage of upper case switching key.
        allowSpecialChars:
            Boolean flag that indicates usage of special char switching key.
        allowSpace:
            Boolean flag that indicates usage of space bar.
        """
        self.rows = []
        self.key_size = key_size
        self.padding = padding
        self.allow_space = allow_space
        self.allow_uppercase = allow_uppercase
        self.allow_special_chars = allow_special_chars
        for model_row in model:
            row = VKeyRow()
            for value in model_row:
                row.add_key(VKey(value))
            self.rows.append(row)
        self.max_length = len(max(self.rows, key=len))
        if self.max_length == 0:
            raise ValueError('Empty layout model provided')

    def configure_specials_key(self, keyboard):
        """ Configures specials key if needed.

        Parameters
        ----------
        keyboard:
            Keyboard instance this layout belong.
        """
        special_row = VKeyRow()
        max_length = self.max_length
        i = len(self.rows) - 1
        current_row = self.rows[i]
        special_keys = [VBackKey()]
        if self.allow_uppercase:
            special_keys.append(VUppercaseKey(keyboard))
        if self.allow_special_chars:
            special_keys.append(VSpecialCharKey(keyboard))
        while len(special_keys) > 0:
            first = False
            while len(special_keys) > 0 and len(current_row) < max_length:
                current_row.add_key(special_keys.pop(0), first=first)
                first = not first
            if i > 0:
                i -= 1
                current_row = self.rows[i]
            else:
                break
        if self.allow_space:
            space_length = len(current_row) - len(special_keys)
            special_row.add_key(VSpaceKey(space_length))
        first = True
        # Adding left to the special bar.
        while len(special_keys) > 0:
            special_row.add_key(special_keys.pop(0), first=first)
            first = not first
        if len(special_row) > 0:
            self.rows.append(special_row)

    def configure_bound(self, surface_size):
        """ Compute keyboard bound regarding of this layout. If `key_size` is
        `None`, then it will compute it regarding of the given surface_size.

        Parameters
        ----------
        surface_size:
            Size of the surface this layout will be rendered on.

        Raises
        ------
        ValueError
            If the layout model is empty.
        """
        r = len(self.rows)
        max_length = self.max_length
        if self.key_size is None:
            self.key_size = (
                surface_size[0]
                - (self.padding * (max_length + 1))) / max_length
        height = self.key_size * r + self.padding * (r + 1)
        if height >= surface_size[1] / 2:
            logger.warning(
                'Computed keyboard height outbound target surface,'
                ' reducing key_size to match')
            self.key_size = (
                (surface_size[1] / 2)
                - (self.padding * (r + 1))) / r
            height = self.key_size * r + self.padding * (r + 1)
            logger.warning('Normalized key_size to %spx' % self.key_size)
        self.set_size((surface_size[0], height), surface_size)

    def set_size(self, size, surface_size):
        """ Sets the size of this layout, and updates
        position, and rows accordingly.

        Parameters
        ----------
        size:
            Size of this layout.
        surface_size:
            Target surface size on which layout will be displayed.
        """
        self.size = size
        self.position = (0, surface_size[1] - self.size[1])
        y = self.position[1] + self.padding
        for row in self.rows:
            r = len(row)
            width = (r * self.key_size) + ((r + 1) * self.padding)
            x = (surface_size[0] - width) / 2
            if row.space is not None:
                x -= ((row.space.length - 1) * self.key_size) / 2
            row.set_size((x, y), self.key_size, self.padding)
            y += self.padding + self.key_size

    def invalidate(self):
        """ Rests all keys states. """
        for row in self.rows:
            for key in row.keys:
                key.state = 0

    def set_uppercase(self, uppercase):
        """ Sets layout uppercase state.

        Parameters
        ----------
        uppercase:
            True if uppercase, False otherwise.
        """
        for row in self.rows:
            for key in row.keys:
                if type(key) == VKey:
                    if uppercase:
                        key.value = key.value.upper()
                    else:
                        key.value = key.value.lower()

    def get_key_at(self, position):
        """ Retrieves if any key is located at the given position

        Parameters
        ----------
        position:
            Position to check key at.

        Returns
        -------
        key:
            The located key if any at the given position, None otherwise.
        """
        for row in self.rows:
            if position in row:
                for key in row.keys:
                    if key.is_touched(position):
                        return key
        return None


def synchronizeLayout(primary, secondary, surface_size):
    """ Synchronizes given layouts by normalizing height by using
    max height of given layouts to avoid transistion dirty effects.

    Parameters
    ----------
    primary:
        Primary layout used.
    secondary:
        Secondary layout used.
    surface_size:
        Target surface size on which layout will be displayed.
    """
    primary.configure_bound(surface_size)
    secondary.configure_bound(surface_size)
    # Check for key size.
    if (primary.key_size < secondary.key_size):
        logging.warning('Normalizing key size from secondary to primary')
        secondary.key_size = primary.key_size
    elif (primary.key_size > secondary.key_size):
        logging.warning('Normalizing key size from primary to secondary')
        primary.key_size = secondary.key_size
    if (primary.size[1] > secondary.size[1]):
        logging.warning('Normalizing layout size from secondary to primary')
        secondary.set_size(primary.size, surface_size)
    elif (primary.size[1] < secondary.size[1]):
        logging.warning('Normalizing layout size from primary to secondary')
        primary.set_size(secondary.size, surface_size)


class VKeyboard(object):
    """
        Virtual Keyboard class.

        A virtual keyboard consists in a VKeyboardLayout that acts as
        the keyboard model and a VKeyboardRenderer which is in charge
        of drawing keyboard component to screen.
    """

    def __init__(
            self,
            surface,
            text_consumer,
            layout,
            special_char_layout=VKeyboardLayout(VKeyboardLayout.SPECIAL),
            renderer=VKeyboardRenderer.DEFAULT):
        """ Default constructor.

        Parameters
        ----------
        surface:
            Surface this keyboard will be displayed at.
        text_consumer:
            Consumer that process text for each update.
        layout:
            Layout this keyboard will use.
        special_char_layout:
            Alternative layout to use, using VKeyboardLayout.SPECIAL
            if not specified.
        renderer:
            Keyboard renderer instance, using VKeyboardStyle.DEFAULT
            if not specified.
        """
        self.surface = surface
        self.text_consumer = text_consumer
        self.renderer = renderer
        self.buffer = u''
        self.state = 0
        self.last_pressed = None
        self.uppercase = False
        self.special_char = False
        self.original_layout = layout
        self.original_layout.configure_specials_key(self)
        self.special_char_layout = special_char_layout
        self.special_char_layout.configure_specials_key(self)
        synchronizeLayout(
            self.original_layout,
            self.special_char_layout,
            self.surface.get_size())
        self.set_layout(layout)

    def invalidate(self):
        """ Invalidates keyboard state, reset layout and redraw. """
        self.layout.invalidate()
        self.draw()

    def set_layout(self, layout):
        """ Sets the layout this keyboard work with.
        Keyboard is invalidate by this action and redraw itself.

        Parameters
        ----------
        layout:
            Layout to set.
        """
        self.layout = layout
        self.invalidate()

    def enable(self):
        """ Sets this keyboard as active. """
        self.state = 1
        self.invalidate()

    def disable(self):
        """ Sets this keyboard as non active. """
        self.state = 0

    def draw(self):
        """ Draw the virtual keyboard into the delegate surface object
        if enabled.
        """
        if self.state > 0:
            self.renderer.draw_background(
                self.surface,
                self.layout.position,
                self.layout.size)
            for row in self.layout.rows:
                for key in row.keys:
                    self.renderer.draw_key(self.surface, key)

    def on_uppercase(self):
        """ Uppercase key press handler. """
        self.uppercase = not self.uppercase
        self.original_layout.set_uppercase(self.uppercase)
        self.special_char_layout.set_uppercase(self.uppercase)
        self.invalidate()

    def on_special_char(self):
        """ Special char key press handler. """
        self.special_char = not self.special_char
        if self.special_char:
            self.set_layout(self.special_char_layout)
        else:
            self.set_layout(self.original_layout)
        self.invalidate()

    def on_event(self, event):
        """Pygame event processing callback method.

        Parameters
        ----------
        event:
            Event to process.
        """
        if self.state > 0:
            if event.type == pygame.MOUSEBUTTONDOWN:
                key = self.layout.get_key_at(pygame.mouse.get_pos())
                if key is not None:
                    self.on_key_down(key)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.on_key_up()
            # elif event.type == pygame.KEYDOWN:
            #    value = pygame.key.name(event.key)
            #    TODO : Find from layout (consider checking layout key space ?)
            # elif event.type == pygame.KEYUP:
            #    value = pygame.key.name(event.key)
            #    TODO : Find from layout (consider checking layout key space ?)

    def set_key_state(self, key, state):
        """Sets the key state and redraws it.

        Parameters
        ----------
        key:
            Key to update state for.
        state:
            New key state.
        """
        key.state = state
        self.renderer.draw_key(self.surface, key)

    def on_key_down(self, key):
        """Process key down event by pressing the given key.

        Parameters
        ----------
        key:
            Key that receives the key down event.
        """
        self.set_key_state(key, 1)
        self.last_pressed = key

    def on_key_up(self):
        """ Process key up event by updating buffer and release key. """
        if (self.last_pressed is not None):
            self.set_key_state(self.last_pressed, 0)
            self.buffer = self.last_pressed.update_buffer(self.buffer)
            self.text_consumer(self.buffer)
            self.last_pressed = None
