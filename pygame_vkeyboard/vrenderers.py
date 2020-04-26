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

    start = max_height // 2
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
                 background_color,
                 background_key_color,
                 background_input_color,
                 background_special_key_color=None):
        """VKeyboardStyle default constructor.

        Parameters
        ----------
        font_name:
            Path to font file for rendering key.
        text_color:
            List of RGB tuples for text color (one value per state).
        cursor_color:
            RGB tuple for cursor color of text input.
        background_color:
            RGB tuple for background color for text.
        background_key_color:
            List of RGB tuples for key background color (one value per state).
        background_input_color:
            RGB tuple for background color of the text input.
        background_special_key_color:
            RGB tuple for special key background color.
        """
        self.font = None
        self.font_input = None
        self.font_name = font_name
        self.text_color = text_color
        self.cursor_color = cursor_color
        self.background_color = background_color
        self.background_key_color = background_key_color
        self.background_input_color = background_input_color
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

    def draw_cursor(self, surface):
        """Default drawing method for cursor of the text input box.

        Cursor is drawn as a simple rectangle filled using the
        cursor color attribute.

        Parameters
        ----------
        surface:
            Surface representing the cursor.
        """
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
        if not self.font_input:  # Initialize font if not done
            self.font_input = fit_font(self.font_name, surface.get_height())
        surface.fill(self.background_input_color)
        surface.blit(self.font_input.render(text, 1, self.text_color[0]), (0, 0))

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
            Surface background should be drawn in.
        key:
            Target key to be drawn.
        special:
            Boolean flag that indicates if the drawn key should use
            special background color if available.
        """
        if not self.font:  # Initialize font if not done
            self.font = fit_font(self.font_name, key.rect.height)

        background_color = self.background_key_color
        if special and self.background_special_key_color is not None:
            background_color = self.background_special_key_color

        surface.fill(background_color[key.state])
        text = self.font.render(str(key), 1, self.text_color[key.state])
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
    background_color=(255, 255, 255),
    background_key_color=((255, 255, 255), (0, 0, 0)),
    background_input_color=(220, 220, 220),
    background_special_key_color=((180, 180, 180), (0, 0, 0))
)

VKeyboardRenderer.DARK = VKeyboardRenderer(
    osp.join(osp.dirname(__file__), 'DejaVuSans.ttf'),
    text_color=((200, 200, 200), (255, 255, 255)),
    cursor_color=(255, 255, 255),
    background_color=(40, 41, 35),
    background_key_color=((65, 66, 67), (47, 48, 51)),
    background_input_color=(80, 80, 80),
    background_special_key_color=((120, 120, 120), (0, 0, 0))
)
