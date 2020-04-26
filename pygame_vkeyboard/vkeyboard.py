#!/usr/bin/env python
# coding: utf8

"""
Visual keyboard for Pygame engine. Aims to be easy to use
as highly customizable as well.

``VKeyboard`` only require a pygame surface to be displayed
on and a text consumer function, as in the following example :

```python
from pygame_vkeyboard import VKeyboard, VKeyboardLayout

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

from . import vkeys
from .vrenderers import VKeyboardRenderer
from .vtextinput import VTextInput, VBackground


# Configure logger.
logging.basicConfig()
logger = logging.getLogger(__name__)


def synchronize_layouts(surface_size, *layouts):
    """Synchronizes given layouts by normalizing height by using
    max height of given layouts to avoid transistion dirty effects.

    Parameters
    ----------
    surface_size:
        Target surface size on which layout will be displayed.
    layouts:
        All layouts to synchronize
    """
    for layout in layouts:
        layout.configure_bound(surface_size)

    layout_ref = min(layouts, key=lambda l: l.key_size)

    for layout in layouts:
        if layout.key_size != layout_ref.key_size:
            logging.warning(
                'Normalizing layout%s key size to %spx (from layout%s)',
                layouts.index(layout),
                layout_ref.key_size,
                layouts.index(layout_ref))
            layout.key_size = layout_ref.key_size
        if layout.size != layout_ref.size:
            logging.warning(
                'Normalizing layout%s size to %s*%spx (from layout%s)',
                layouts.index(layout),
                layout_ref.size[0], layout_ref.size[1],
                layouts.index(layout_ref))

        # Compute all internal values of the layout
        layout.set_size(layout_ref.size, surface_size)


class VKeyRow(object):
    """A VKeyRow defines a keyboard row which is composed of a list of
    VKey.

    This class aims to be created internally after parsing a keyboard
    layout model. It is used to optimize collision detection, by first
    checking row collision, then internal row key detection.
    """

    def __init__(self):
        """Default row constructor. """
        self.keys = []
        self.height = 0
        self.position = (0, 0)
        self.space = None

    def add_key(self, key, first=False):
        """Adds the given key to this row.

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
        if isinstance(key, vkeys.VSpaceKey):
            self.space = key

    def set_size(self, position, size, padding):
        """Row size setter. The size correspond to the row height, since the
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
            key.set_size(size, size)
            key.set_position(x, position[1])
            x += padding + key.rect.width

    def __len__(self):
        """len() operator overload.

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

    # AZERTY Layout.
    AZERTY = ['1234567890', 'azertyuiop', 'qsdfghjklm', 'wxcvbn']

    # QWERTY Layout.
    QWERTY = ['1234567890', 'qwertyuiop', 'asdfghjkl', 'wzxcvbnm']

    # Number only layout.
    NUMBER = ['123', '456', '789', '0']

    # TODO : Insert special characters layout which include number.
    SPECIAL = [u'&é"\'(§è!çà)', u'°_-^$¨*ù`%£', u',;:=?.@+<>#', u'[]{}/\\|']
    """Special characters layout. """

    def __init__(self,
                 model,
                 key_size=None,
                 padding=5,
                 allow_uppercase=True,
                 allow_special_chars=True,
                 allow_space=True):
        """Default constructor. Initializes layout rows.

        Parameters
        ----------
        model:
            Layout model to use.
        key_size:
            Size of the key, if not specified will be computed dynamically.
        padding:
            Padding between key (work horizontally as vertically).
        allow_uppercase:
            Boolean flag that indicates usage of upper case switching key.
        allow_special_chars:
            Boolean flag that indicates usage of special char switching key.
        allow_space:
            Boolean flag that indicates usage of space bar.

        Raises
        ------
        ValueError
            If the layout model is empty.
        """
        self.position = None
        self.size = None
        self.rows = []
        self.sprites = pygame.sprite.LayeredDirty()
        self.key_size = key_size
        self.padding = padding
        self.allow_space = allow_space
        self.allow_uppercase = allow_uppercase
        self.allow_special_chars = allow_special_chars
        for model_row in model:
            row = VKeyRow()
            for value in model_row:
                key = vkeys.VKey(value)
                row.add_key(key)
                self.sprites.add(key, layer=1)
            self.rows.append(row)
        self.max_length = len(max(self.rows, key=len))
        if self.max_length == 0:
            raise ValueError('Empty layout model provided')

    def hide(self):
        """Hide all keys."""
        for sprite in self.sprites:
            sprite.visible = 0

    def show(self):
        """Show all keys."""
        for sprite in self.sprites:
            sprite.visible = 1

    def configure_renderer(self, renderer):
        """Configure the keys with the given renderer.

        Parameters
        ----------
        renderer:
            Renderer instance this layout uses.
        """
        for key in self.sprites.get_sprites_from_layer(1):
            key.renderer = renderer

    def configure_special_keys(self, keyboard):
        """Configures specials key if needed.

        Parameters
        ----------
        keyboard:
            Keyboard instance this layout belong.
        """
        special_row = VKeyRow()
        max_length = self.max_length
        i = len(self.rows) - 1
        current_row = self.rows[i]

        # Create special keys list
        special_keys = [vkeys.VBackKey()]
        if self.allow_uppercase:
            special_keys.append(
                vkeys.VUppercaseKey(keyboard.on_uppercase, keyboard))
        if self.allow_special_chars:
            special_keys.append(
                vkeys.VSpecialCharKey(keyboard.on_special_char, keyboard))
        self.sprites.add(*special_keys, layer=1)

        # Dispatch special keys in the layout
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
            special_row.add_key(vkeys.VSpaceKey(space_length))
            self.sprites.add(special_row.space, layer=1)
        first = True

        # Adding left to the special bar.
        while len(special_keys) > 0:
            special_row.add_key(special_keys.pop(0), first=first)
            first = not first
        if len(special_row) > 0:
            self.rows.append(special_row)

    def configure_bound(self, surface_size):
        """Compute keyboard bound regarding of this layout. If `key_size` is
        `None`, then it will compute it regarding of the given surface_size.

        Parameters
        ----------
        surface_size:
            Size of the surface this layout will be rendered on.
        """
        r = len(self.rows)
        if self.key_size is None:
            self.key_size = int(
                (surface_size[0] - (self.padding * (self.max_length + 1)))
                / self.max_length)
        height = self.key_size * r + self.padding * (r + 1)
        if height >= surface_size[1] / 2:
            self.key_size = int(((surface_size[1] / 2)
                                 - (self.padding * (r + 1))) / r)
            height = self.key_size * r + self.padding * (r + 1)
            logger.warning('Computed layout height outbound target surface,'
                           ' reducing key_size to %spx', self.key_size)
        self.set_size((surface_size[0], int(height)), surface_size)

    def set_size(self, size, surface_size):
        """Sets the size of this layout, and updates
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

    def set_uppercase(self, uppercase):
        """Sets layout uppercase state.

        Parameters
        ----------
        uppercase:
            True if uppercase, False otherwise.
        """
        for key in self.sprites.get_sprites_from_layer(1):
            key.set_uppercase(uppercase)

    def get_key(self, value):
        """Retrieves if any key with the given value

        Parameters
        ----------
        value:
            Value to find among keys.

        Returns
        -------
        key:
            The located key if any with the given value, None otherwise.
        """
        for key in self.sprites.get_sprites_from_layer(1):
            if key.value == value:
                return key
        return None

    def get_key_at(self, position):
        """Retrieves if any key is located at the given position

        Parameters
        ----------
        position:
            Position to check key at.

        Returns
        -------
        key:
            The located key if any at the given position, None otherwise.
        """
        for sprite in self.sprites.get_sprites_at(position):
            if isinstance(sprite, vkeys.VKey):
                return sprite


class VKeyboard(object):
    """
    Virtual Keyboard class.

    A virtual keyboard consists in a VKeyboardLayout that acts as
    the keyboard model and a VKeyboardRenderer which is in charge
    of drawing keyboard component to screen.
    """

    def __init__(self,
                 surface,
                 text_consumer,
                 layout,
                 special_char_layout=VKeyboardLayout(VKeyboardLayout.SPECIAL),
                 renderer=VKeyboardRenderer.DEFAULT,
                 show_text_input=False):
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
            Keyboard renderer instance, using VKeyboardRenderer.DEFAULT
            if not specified.
        """
        self.surface = surface
        self.text_consumer = text_consumer
        self.renderer = renderer
        self.state = 0
        self.last_pressed = None
        self.uppercase = False
        self.special_char = False

        self.layout = layout
        self.original_layout = layout
        self.original_layout.configure_special_keys(self)
        self.original_layout.configure_renderer(self.renderer)

        self.special_char_layout = special_char_layout
        self.special_char_layout.configure_special_keys(self)
        self.special_char_layout.configure_renderer(self.renderer)

        synchronize_layouts(self.surface.get_size(), self.original_layout,
                            self.special_char_layout)

        self.background = VBackground(
            self.surface.get_rect().size,
            self.renderer)
        self.background.set_rect(*self.layout.position + self.layout.size)
        self.original_layout.sprites.add(self.background, layer=0)
        self.special_char_layout.sprites.add(self.background, layer=0)

        self.input = VTextInput((
            self.original_layout.position[0],
            self.original_layout.position[1] - self.original_layout.key_size),
            (self.original_layout.size[0], self.original_layout.key_size))

        if show_text_input:
            self.input.enable()

    def set_layout(self, layout):
        """Sets the layout this keyboard work with.
        Keyboard is invalidate by this action and redraw itself.

        Parameters
        ----------
        layout:
            Layout to set.
        """
        self.layout.hide()
        self.layout = layout
        self.layout.show()

    def enable(self):
        """Sets this keyboard as active. """
        self.state = 1

    def disable(self):
        """Sets this keyboard as non active. """
        self.state = 0

    def draw(self, surface=None, force=False):
        """Draw the virtual keyboard.

        This method is optimized to be called at each loop of the
        main application. It uses DirtySprite to update only parts
        of the screen that need to be refreshed.

        Parameters
        ----------
        surface:
            Surface this keyboard will be displayed at.
        force:
            Force the drawing of the entire surface (time consuming).

        Returns
        -------
        rects:
            List of updated area.
        """
        rects = []
        if self.state > 0:
            rects += self.layout.sprites.draw(surface or self.surface)
            rects += self.input.draw(surface or self.surface, force)
            if force:
                self.layout.sprites.repaint_rect(self.background.rect)
        return rects

    def update(self, events):
        """Pygame events processing callback method.

        Parameters
        ----------
        events:
            List of events to process.
        """
        if self.state > 0:
            self.layout.sprites.update(events)
            self.input.update(events)

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    key = self.layout.get_key_at(event.pos)
                    if key:
                        self.on_key_down(key)
                elif event.type == pygame.KEYDOWN:
                    key = self.layout.get_key(event.unicode or event.key)
                    if key:
                        self.on_key_down(key)

    def on_event(self, event):
        """Deprecated method, only for backward compatibility."""
        self.update((event,))
        self.draw()

    def on_uppercase(self):
        """Uppercase key press handler."""
        self.uppercase = not self.uppercase
        self.original_layout.set_uppercase(self.uppercase)
        self.special_char_layout.set_uppercase(self.uppercase)

    def on_special_char(self):
        """Special char key press handler."""
        self.special_char = not self.special_char
        if self.special_char:
            self.set_layout(self.special_char_layout)
        else:
            self.set_layout(self.original_layout)

    def on_key_down(self, key):
        """Process key down event by pressing the given key.

        Parameters
        ----------
        key:
            Key that receives the key down event.
        """
        if isinstance(key, vkeys.VBackKey):
            self.input.delete_at_cursor()
        else:
            text = key.update_buffer('')
            if text:
                self.input.add_at_cursor(text)

        if not isinstance(key, vkeys.VActionKey):
            self.text_consumer(self.input.text)
