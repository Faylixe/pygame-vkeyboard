#!/usr/bin/env python
# coding: utf8

"""
Renderer for the keyboard and the text box used to display
the current text.
"""

import os.path as osp
import pygame  # pylint: disable=import-error

from . import vkeys


def fit_font(font_name, max_height):
    """Set the size of the font to fit the given height.

    Parameters
    ----------
    font_name:
        Path to font file for rendering key.
    max_height:
        Height to fit.
    """
    font = pygame.font.Font(font_name, 1)

    # Ensure a large panel of characters heights
    text = "?/|!()§&@0123456789azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN"  # noqa

    start = 0
    end = max_height * 2

    while start < end:
        k = (start + end) // 2
        font = pygame.font.Font(font_name, k)
        height = font.size(text)[1]
        if height > max_height:
            end = k
        else:
            start = k + 1

    return font


def draw_round_rect(surface, color, rect, radius=0.1):
    """Draw a rounded rectangle.

    Parameters
    ----------
    surface:
        Surface to draw on.
    color:
        RGBA tuple color to draw with, the alpha value is optional.
    rect:
        Rectangle to draw, position and dimensions.
    radius:
        Used for drawing rectangle with rounded corners. The supported range is
        [0, 1] with 0 representing a rectangle without rounded corners.
    """
    rect = pygame.Rect(rect)
    if len(color) == 4:
        alpha = color[-1]
        color = color[:3] + (0,)
    else:
        alpha = 255
        color += (0,)

    pos = rect.topleft
    rect.topleft = 0, 0
    rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

    circle = pygame.Surface([min(rect.size) * 3] * 2, pygame.SRCALPHA)
    pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
    circle = pygame.transform.smoothscale(circle,
                                          [int(min(rect.size) * radius)] * 2)

    radius = rectangle.blit(circle, (0, 0))
    radius.bottomright = rect.bottomright
    rectangle.blit(circle, radius)
    radius.topright = rect.topright
    rectangle.blit(circle, radius)
    radius.bottomleft = rect.bottomleft
    rectangle.blit(circle, radius)

    rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
    rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

    rectangle.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
    rectangle.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)

    return surface.blit(rectangle, pos)


class VKeyboardRenderer(object):
    """
    A VKeyboardRenderer is in charge of keyboard rendering.

    It handles keyboard rendering properties such as color or padding,
    and provides several rendering methods.

    .. note::
        A DEFAULT and DARK styles are available as class attribute.
    """

    DEFAULT = None
    DARK = None

    def __init__(self,
                 font_name,
                 text_color,
                 cursor_color,
                 selection_color,
                 background_color,
                 background_key_color,
                 background_input_color,
                 text_special_key_color=None,
                 background_special_key_color=None):
        """VKeyboardStyle default constructor.

        Some parameters take a list of color tuples, one per state.
        The states are: (released, pressed)

        Parameters
        ----------
        font_name:
            Path to font file for rendering key.
        text_color:
            List of RGB tuples for text color (one tuple per state).
        cursor_color:
            RGB tuple for cursor color of text input.
        selection_color:
            RGB tuple for selected key color.
        background_color:
            RGB tuple for background colo   r for text.
        background_key_color:
            List of RGB tuples for key background color (one tuple per state).
        background_input_color:
            RGB tuple for background color of the text input.
        text_special_key_color:
            List of RGB tuples for special key text color (one tuple per state).
        background_special_key_color:
            List of RGB tuples for special key background color (one tuple per
            state).
        """
        self.font = None
        self.font_height = None
        self.font_input = None
        self.font_input_height = None
        self.font_name = font_name
        self.text_color = text_color
        self.cursor_color = cursor_color
        self.selection_color = selection_color
        self.background_color = background_color
        self.background_key_color = background_key_color
        self.background_input_color = background_input_color

        self.text_special_key_color = text_special_key_color
        self.background_special_key_color = background_special_key_color

    def get_text_width(self, text):
        """Return the width of the given text in the text input box.

        Parameters
        ----------
        text:
            Text to evaluate.
        """
        return self.font_input.size(text)[0]

    def truncate(self, text, max_width, start=0, nearest=False):
        """Truncate the given text in order to fit the maximum
        given width.

        This function uses the binary search algorithm to go faster
        than a one-by-one try.

        Parameters
        ----------
        text:
            Text to split.
        max_width:
            Maximum authorized width of the text (according to font).
        start:
            Index for searching the text part with correct width.
        nearest:
            If True, the returned text can have a width higher than
            the ``max_width`` to reduce abs(max_width - width).

        Returns
        -------
        (part, width):
            Truncated text and its rendered width.
        """
        width = 0
        end = len(text)

        if end < start:
            return text, self.get_text_width(text)

        while start < end:
            k = (start + end) // 2
            new_width = self.get_text_width(text[:k+1])
            if new_width > max_width:
                end = k
            else:
                width = new_width
                start = k + 1

        if nearest:
            next_width = self.get_text_width(text[:start+1])
            if abs(max_width - next_width) < abs(max_width - width):
                return text[:start+1], next_width

        return text[:start], width

    def draw_background(self, surface):
        """Default drawing method for background.

        Background is drawn as a simple rectangle filled using this
        style background color attribute.

        Parameters
        ----------
        surface:
            Surface background should be drawn in.
        """
        surface.fill(self.background_color)

    def draw_cursor(self, surface, cursor):
        """Default drawing method for cursor of the text input box.

        Cursor is drawn as a simple rectangle filled using the
        cursor color attribute.

        Parameters
        ----------
        surface:
            Surface representing the cursor.
        cursor:
            Cursor object.
        """
        if cursor.selected:
            surface.fill(self.selection_color)
        else:
            surface.fill(self.cursor_color)

    def draw_text(self, surface, text):
        """Default drawing method for text input box.

        Draw the text.

        Parameters
        ----------
        surface:
            Surface on which the text is drawn.
        text:
            Target text to be drawn.
        """
        if self.font_input_height != surface.get_height():
            # Resize font to fit the surface
            self.font_input = fit_font(self.font_name, surface.get_height())
            self.font_input_height = surface.get_height()

        surface.fill(self.background_input_color)
        surface.blit(self.font_input.render(text, 1,
                                            self.text_color[0]), (0, 0))

    def draw_key(self, surface, key):
        """Default drawing method for key.

        Draw the key accordingly to it type.

        Parameters
        ----------
        surface:
            Surface background should be drawn in.
        key:
            Target key to be drawn.
        """
        if isinstance(key, vkeys.VSpaceKey):
            self.draw_space_key(surface, key)
        elif isinstance(key, vkeys.VBackKey):
            self.draw_back_key(surface, key)
        elif isinstance(key, vkeys.VUppercaseKey):
            self.draw_uppercase_key(surface, key)
        elif isinstance(key, vkeys.VSpecialCharKey):
            self.draw_special_char_key(surface, key)
        else:
            self.draw_character_key(surface, key)

    def draw_character_key(self, surface, key, special=False):
        """Default drawing method for key.

        Key is drawn as a simple rectangle filled using this
        cell style background color attribute. Key value is printed
        into drawn cell using internal font.

        Parameters
        ----------
        surface:
            Surface key background should be drawn in.
        key:
            Target key to be drawn.
        special:
            Boolean flag that indicates if the drawn key should use
            special background color if available.
        """
        rect = surface.get_rect().inflate(-2, -2)
        if self.font_height != rect.height:
            # Resize font to fit the surface
            self.font = fit_font(self.font_name, rect.height)
            self.font_height = rect.height

        background_color = self.background_key_color[key.pressed]
        if special and self.background_special_key_color:
            background_color = self.background_special_key_color[key.pressed]

        text_color = self.text_color[key.pressed]
        if special and self.text_special_key_color and not key.pressed:
            # Key is not pressed, color according to activated state
            state = getattr(key, 'activated', key.pressed)
            text_color = self.text_special_key_color[state]

        if key.selected:
            surface.fill(self.selection_color)
        else:
            surface.fill(self.background_color)

        draw_round_rect(surface, background_color, rect, 0.3)
        text = self.font.render(str(key), 1, text_color)
        x = (key.rect.width - text.get_width()) // 2
        y = (key.rect.height - text.get_height()) // 2
        surface.blit(text, (x, y))

    def draw_space_key(self, surface, key):
        """Default drawing method space key.

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
        """Default drawing method for back key. Drawn as character key.

        Parameters
        ----------
        surface:
            Surface background should be drawn in.
        key:
            Target key to be drawn.
        """
        self.draw_character_key(surface, key, True)

    def draw_uppercase_key(self, surface, key):
        """Default drawing method for uppercase key. Drawn as character key.

        Parameters
        ----------
        surface:
            Surface background should be drawn in.
        key:
            Target key to be drawn.
        """
        self.draw_character_key(surface, key, True)

    def draw_special_char_key(self, surface, key):
        """Default drawing method for special char key.
        Drawn as character key.

        Parameters
        ----------
        surface:
            Surface background should be drawn in.
        key:
            Target key to be drawn.
        """
        self.draw_character_key(surface, key, True)


# Default keyboard renderer
VKeyboardRenderer.DEFAULT = VKeyboardRenderer(
    osp.join(osp.dirname(__file__), 'DejaVuSans.ttf'),
    text_color=((0, 0, 0), (255, 255, 255)),
    cursor_color=(0, 0, 0),
    selection_color=(0, 0, 200),
    background_color=(255, 255, 255),
    background_key_color=((255, 255, 255), (0, 0, 0)),
    background_input_color=(220, 220, 220),
    background_special_key_color=((180, 180, 180), (0, 0, 0))
)

VKeyboardRenderer.DARK = VKeyboardRenderer(
    osp.join(osp.dirname(__file__), 'DejaVuSans.ttf'),
    text_color=((182, 183, 184), (255, 255, 255)),
    cursor_color=(255, 255, 255),
    selection_color=(124, 183, 62),
    background_color=(0, 0, 0),
    background_key_color=((59, 56, 54), (47, 48, 51)),
    background_input_color=(80, 80, 80),
    text_special_key_color=((182, 183, 184), (124, 183, 62)),
    background_special_key_color=((35, 33, 30), (47, 48, 51))
)
