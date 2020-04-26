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
    and provides two rendering methods : one for the keyboard
    background and another one the the key rendering.

    .. note::
        A DEFAULT style instance is available as class attribute.
    """

    DEFAULT = None

    def __init__(self,
                 font_name,
                 background_color,
                 key_background_color,
                 text_color,
                 special_key_background_color=None):
        """VKeyboardStyle default constructor.

        Parameters
        ----------
        font_name:
            Path to font file for rendering key.
        background_color:
            RGB tuple for background color.
        key_background_color:
            List of RGB tuples for key background color (one value per state).
        text_color:
            List of RGB tuples for key text color (one value per state).
        special_key_background_color:
            RGB tuple for special key background color.
        """
        self.font = None
        self.font_name = font_name
        self.background_color = background_color
        self.key_background_color = key_background_color
        self.special_key_background_color = special_key_background_color
        self.text_color = text_color

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

        background_color = self.key_background_color
        if special and self.special_key_background_color is not None:
            background_color = self.special_key_background_color

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
    (255, 255, 255),
    ((255, 255, 255), (0, 0, 0)),
    ((0, 0, 0), (255, 255, 255)),
    ((180, 180, 180), (0, 0, 0)))


class VTextInputRenderer(object):
    """
    A VTextInputRenderer is in charge of text input rendering.

    It handles text rendering properties such as color and font,
    and provides three rendering methods : one for the borders,
    one for the background and the last for the text rendering.

    .. note::
        A DEFAULT style instance is available as class attribute.
    """

    DEFAULT = None

    def __init__(self,
                 font_name,
                 text_color,
                 cursor_color,
                 border_color,
                 background_color):
        """
        Parameters
        ----------
        font_name:
            Path to font file for rendering key.
        text_color:
            RGB tuple for text color.
        cursor_color:
            RGB tuple for cursor color.
        border_color:
            RGB tuple for border line color.
        background_color:
            RGB tuple for background color for text.
        """
        self.font = None
        self.font_name = font_name
        self.text_color = text_color
        self.cursor_color = cursor_color
        self.border_color = border_color
        self.background_color = background_color

    def get_text_width(self, text):
        """Return the width of the given text.

        Parameters
        ----------
        text:
            Text to evaluate.
        """
        return self.font.size(text)[0]

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
        """Default drawing method for borders.

        Borders is drawn as a simple background rectangle filled using the
        border color attribute.

        Parameters
        ----------
        surface:
            Surface representing the borders.
        """
        surface.fill(self.border_color)

    def draw_cursor(self, surface):
        """Default drawing method for cursor.

        Cursor is drawn as a simple rectangle filled using the
        cursor color attribute.

        Parameters
        ----------
        surface:
            Surface representing the cursor.
        """
        surface.fill(self.cursor_color)

    def draw_text(self, surface, text):
        """Default drawing method for text.

        Draw the text.

        Parameters
        ----------
        surface:
            Surface on which the text is drawn.
        text:
            Target text to be drawn.
        """
        if not self.font:  # Initialize font if not done
            self.font = fit_font(self.font_name, surface.get_height())
        surface.fill(self.background_color)
        surface.blit(self.font.render(text, 1, self.text_color), (0, 0))


# Default text renderer
VTextInputRenderer.DEFAULT = VTextInputRenderer(
    osp.join(osp.dirname(__file__), 'DejaVuSans.ttf'),
    (0, 0, 0), (0, 0, 0), (255, 255, 255), (220, 220, 220))
