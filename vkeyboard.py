#!/usr/bin/python

""" Module doc. """

import pygame
from pygame.locals import *

pygame.font.init()

class VKeyboardRenderer(object):
    """A VKeyboardRenderer is in charge of keyboard rendering.

    It handles keyboard rendering properties such as color or padding,
    and provides two rendering methods : one for the keyboard background
    and another one the the key rendering.
    
    .. note::
        A DEFAULT style instance is available as class attribute.
    """

    def __init__(self, font, keyboard_background_color, key_background_color, text_color, padding):
        """VKeyboardStyle default constructor. 
        
        :param font: Used font for rendering key.
        :param keyboard_background_color: Background color use for the keyboard.
        :param key_background_color: Tuple of background color for key (one value per state).
        :param text_color: Tuple of key text color (one value per state).
        :param padding: Padding between key (work horizontally as vertically).
        """
        self.font = font
        self.keyboard_background_color = keyboard_background_color
        self.key_background_color = key_background_color
        self.text_color = text_color
        self.padding = padding
        
    def draw_background(self, surface, position, size):
        """Default drawing method for background.

        Background is drawn as a simple rectangle filled using this
        style background color attribute.

        :param surface: Surface background should be drawn in.
        :param position: Surface relative position the keyboard should be drawn at.
        :param size: Expected size of the drawn keyboard.
        """
        pygame.draw.rect(surface, self.keyboard_background_color, position + size)
    
    def draw_key(self, surface, key):
        """Default drawing method for key. 

        Key is drawn as a simple rectangle filled using this
        cell style background color attribute. Key value is printed
        into drawn cell using internal font.

        :param surface: Surface background should be drawn in.
        :param key: Target key to be drawn.
        """
        pygame.draw.rect(surface, self.key_background_color[key.state], key.position + (key.size, key.size))
        # TODO : Center key into cell.
        return surface.blit(self.font.render(key.value, 1, self.text_color[key.state], None), key.position)

""" Default style implementation. """
VKeyboardRenderer.DEFAULT = VKeyboardStyle(
    pygame.font.SysFont('arial', 20),
    (50, 50, 50),
    ((255, 255, 255), (0, 0, 0)),
    ((0, 0, 0), (255, 255, 255)),
    5
)

class VKey(object):
    """Simple key holder class.

    Holds key information (its value), as it's state, 1 for pressed,
    0 for released. Also contains it size / position properties.
    """

    def __init__(self, value):
        """Default key constructor.

        :param value: Value of this key which also is the label displayed to the screen.
        """
        self.state = 0
        self.value = value
        self.position = (-1, -1)
        self.size = 0

    def is_touched(self, position):
        """Hit detection method.
        
        Indicates if this key has been hit by a touch / click event at the given position.

        :param position: Event position.
        :returns: True is the given position collide this key, False otherwise.
        """
        return position[0] >= self.position[0] and position[0] <= self.position[0]+ self.size
    
    def update_buffer(self, buffer):
        """Text update method.
        
        Aims to be called internally when a key collision has been detected.
        Updates and returns the given buffer using this key value.

        :param buffer: Buffer to be updated.
        :returns: Updated buffer value.
        """
        return buffer + self.value

class VKeyRow(object):
    """A VKeyRow defines a keyboard row which is composed of a list of VKey.
    
    This class aims to be created internally after parsing a keyboard layout model.
    It is used to optimize collision detection, by first checking row collision,
    then internal row key detection.
    """

    def __init__(self):
        """ Default row constructor. """
        self.keys = []
        self.y = -1
        self.height = 0

    def add_key(self, key):
        """Adds the given key to this row.

        :param key: Key to be added to this row.
        """
        self.keys.append(key)

    def set_size(self, y, size, padding):
        """Row size setter.

        The size correspond to the row height, since the row width is constraint
        to the surface width the associated keyboard belongs. Once size is settled,
        the size for each child keys is associated.
        
        :param y:
        :param size:
        :param padding:
        """
        self.height = size
        self.y = y
        x = padding
        for key in self.keys:
            key.size = size
            key.position = (x, y)
            x += padding + size

    def __contains__(self, position):
        """Indicates if the given position collide this row.
        
        :param position: Position to check againt this row.
        :returns: True if the given position collide this row, False otherwise.
        """
        return position[1] >= self.y and position[1] <= self.y + self.height

    def __len__(self):
        """len() operator overload.

        :returns: Number of keys thi row contains.
        """
        return len(self.keys)

class VKeyboardLayout(object):
    """Keyboard layout class.
    
    A keyboard layout is built using layout model which consists in an
    list of supported character. Such list item as simple string containing
    characters assigned to a row.

    An erasing key is inserted automatically to the first row.

    If allowUpperCase flag is True, then an upper case key will be inserted at
    the beginning of the second row.

    If allowSpecialChars flag is True, then an special characters / number key will
    be inserted at the beginning of the third row. Pressing this key will switch the
    associated keyboard current layout.
    """

    """ Azerty layout. """
    AZERTY = ['azertyuiop', 'qsdfghjklm', 'wxcvbn']

    """ Number only layout. """ 
    NUMBER = ['123', '456', '789', '0']

    # TODO : Insert special characters layout which include number.

    def __init__(self, model, key_size=None, allow_uppercase=True, allow_special_chars=True):
        """Default constructor. Initializes layout rows.
        
        :param model: Layout model to use.
        :param key_size Size of the key, if not specified will be computed dynamically.
        :param allowUpperCase: Boolean flag that indicates usage of upper case switching key.
        :param allowSpecialChars: Boolean flag that indicates usage of special char switching key.
        """
        self.rows = []
        self.key_size = key_size
        i = 0
        for model_row in model:
            row = VKeyRow()
            if i == 0: row.add_key(VKey('<-')) # Back key.
            elif i == 1 and allow_uppercase: row.add_key(VKey('MAJ')) # Majlock.
            elif i == 2 and allow_special_chars: row.add_key(VKey('123')) # Special chars.
            for value in model_row:
                row.add_key(VKey(value))
            self.rows.append(row)
            i += 1

    def configure_bound(self, surface_size, padding):
        """Compute keyboard bound regarding of this layout.
        
        If key_size is None, then it will compute it regarding of the given surface_size.

        :param surface_size: Size of the surface this layout will be rendered on.
        :param padding: Padding between key (work horizontally as vertically).
        """
        if self.key_size is None:
            max_length = len(max(self.rows, key=len))
            self.key_size = (surface_size[0] - (padding * (max_length + 1))) / max_length
        height = self.key_size * len(self.rows) + padding * (len(self.rows) + 1)
        self.size = (surface_size[0], height)
        self.position = (0, surface_size[1] - self.size[1])
        # TODO : Check if the size do not outbound the target surface and warn ?
        y = self.position[1] + padding
        for row in self.rows:
            row.set_size(y, self.key_size, padding)
            y += padding + self.key_size

    def get_key_at(self, position):
        """Retrieves if any key is located at the given position
        
        :param position: Position to check key at.
        :returns: The located key if any at the given position, None otherwise.
        """
        for row in self.rows:
            if position in row:
                for key in row.keys:
                    if key.is_touched(position):
                        return key
        return None

class VKeyboard(object):
    """Virtual Keyboard class.
    
    A virtual keyboard consists in a VKeyboardLayout that acts as the keyboard model
    and a VKeyboardRenderer which is in charge of drawing keyboard component to screen. 
    """

    def __init__(self, surface, text_consumer, layout, renderer=VKeyboardRenderer.DEFAULT):
        """Default constructor.
        
        :param surface: Surface this keyboard will be displayed at.
        :param text_consumer: Consumer that process text for each update.
        :param layout: Layout this keyboard will use.
        :param renderer: Keyboard renderer instance, using VKeyboardStyle.DEFAULT if not specified.
        """
        self.surface = surface
        self.text_consumer = text_consumer
        self.layout = layout
        self.renderer = renderer
        self.buffer = ''
        self.state = 0
        layout.configure_bound(surface.get_size(), style.padding)

    def enable(self):
        """ Sets this keyboard as active. """
        self.state = 1
    
    def disable(self):
        """ Sets this keyboard as non active. """
        self.state = 0

    def draw(self):
        """ Draw the virtual keyboard into the delegate surface object if enabled. """
        if self.state > 0:
            self.renderer.draw_background(self.surface, self.layout.position, self.layout.size)
            for row in self.layout.rows:
                for key in row.keys:
                    self.renderer.draw_key(self.surface, key)

    def on_event(self, event):
        """

        :param event:
        """
        if self.state > 0:
            if event.type == MOUSEBUTTONDOWN:
                key = self.layout.get_key_at(position)
                if key is not None:
            elif event.type == MOUSEBUTTONUP:
                key = self.layout.get_key_at(position)
                if key is not None:
                    self.on_key_up(key)
            elif event.type == KEYDOWN:
                value = pygame.key.name(event.key)
                # TODO : Find from layout (consider checking layout key space ?)
            elif event.type == KEYUP:
                value = pygame.key.name(event.key)
                # TODO : Find from layout (consider checking layout key space ?)
                
    def set_key_state(self, key, state):
        """

        :param key:
        :param state:
        """
        key.state = state
        self.renderer.draw_key(self.surface, key)

    def on_key_down(self, key):
        """
        
        :param key: 
        """
        self.set_key_state(key, 1)

    def on_key_up(self, key):
        """
        
        :param key: 
        """
        self.buffer = key.update_buffer(self.buffer)
        self.text_consumer(self.buffer)
        self.set_key_state(key, 0)
