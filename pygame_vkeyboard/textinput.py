# coding: utf8


import os.path as osp
import textwrap
import pygame


class TextInputRenderer(object):

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
        font:
            Used font for rendering text.
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

    def fit_font(self, size):
        """Set the size of the font to fit the rectangle with
        the given size.

        It returns an average of the number of characters to
        fill the rectangle width.

        Parameters
        ----------
        size:
            Size of the rectangle to fit
        """
        self.font = pygame.font.Font(self.font_name, 1)

        # Attempt to figure out how many chars will fit on a line
        # this does not work with proportional fonts
        text = "0123456789azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN"  # 10 + 2*26 chars
        i = 0
        text_width = 0
        text_height = 0
        while text_height < size[1]:
            text_width, text_height = self.font.size(text)
            self.font = pygame.font.Font(self.font_name, i)
            i += 1
        return int(size[0] / (text_width / (10 + 2*26))) - 1  # Average chars per line (horizontal)

    def draw_background(self, surface, position, size):
        """Default drawing method for background.

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
        # Draw border
        pygame.draw.rect(surface,  self.border_color, position + size)
        # Draw text background
        pygame.draw.rect(surface,  self.background_color,
                         (position[0] + 1, position[1] + 1) + (size[0] - 2, size[1] - 2))

    def draw_cursor(self, surface, position, cursor):
        """Default drawing method for cursor.

        Cursor is drawn as a simple rectangle filled using this
        cursor color attribute.

        Parameters
        ----------
        surface:
            Surface background should be drawn in.
        position:
            Surface relative position the keyboard should be drawn at.
        cursor:
            Cursor element to be drawn.
        """
        if cursor.state:
            pygame.draw.rect(surface,
                             self.cursor_color,
                             (position[0], position[1] + 4) +
                             (cursor.size[0], cursor.size[1] - 8))

    def draw_text(self, surface, position, text):
        """Default drawing method for text.

        Draw the text.

        Parameters
        ----------
        surface:
            Surface background should be drawn in.
        position:
            Surface relative position the keyboard should be drawn at.
        text:
            Target text to be drawn.
        """
        surface.blit(self.font.render(text, 1, self.text_color), position)


# Default text renderer
pygame.font.init()
TextInputRenderer.DEFAULT = TextInputRenderer(
    osp.join(osp.dirname(__file__), 'DejaVuSans.ttf'),
    (255, 255, 255), (255, 255, 255), (255, 255, 255), (0, 0, 0))


class TextInputCursor(object):
    """
    Handles the cursor.

    Holds cursor information (its position), as it's state, 1 for visible,
    0 for hidden. Also contains it size / position properties.

    The ``index`` represente the absolute position. The ``line_index`` is
    the position in the current line.
    """

    def __init__(self, size, max_line_chars):
        self.state = 1
        self.size = size
        self.line = 0
        self.index = 0
        self.line_index = 0
        self.max_line_chars = max_line_chars

        # Blink management
        self.clock = pygame.time.Clock()
        self.switch_ms = 500
        self.switch_counter = 0

    def set_index(self, index, line=0):
        """Move the cursor at the given index"""
        self.index = line * self.max_line_chars + index
        self.line = self.index // self.max_line_chars
        self.line_index = self.index % self.max_line_chars

    def increment(self, step=1, position_max=None):
        """Move the cursor of one or more steps (but not beyond the position_max)"""
        pos = max(0, self.index + step)
        if position_max is None:
            position_max = pos
        self.index = min(pos, position_max)
        self.line = self.index // self.max_line_chars
        self.line_index = self.index % self.max_line_chars

    def toggle(self):
        """Toggle visibility of the cursor"""
        old = self.state
        self.clock.tick()
        self.switch_counter += self.clock.get_time()
        if self.switch_counter >= self.switch_ms:
            self.switch_counter %= self.switch_ms
            self.state = int(not self.state)
        return self.state != old


class TextInput(object):
    """
    Handles the text input box.
    """

    def __init__(self, surface, position, size, renderer=TextInputRenderer.DEFAULT):
        self.state = 0
        self.surface = surface
        self.position = position
        self.size = size
        self.text = ''
        self.text_margin = 2
        self.renderer = renderer
        self.max_line_chars = self.renderer.fit_font((size[0] - self.text_margin * 2,
                                                      size[1] - self.text_margin * 2))

        self.cursor = TextInputCursor((2, size[1]), self.max_line_chars)

    def enable(self):
        """Set this text input as active."""
        self.state = 1

    def disable(self):
        """Set this text input as non active."""
        self.state = 0

    def on_event(self, event):
        """Pygame event processing callback method.

        Parameters
        ----------
        event:
            Event to process.
        """
        if self.state > 0:
            if self.cursor.toggle():
                self.draw()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.cursor.increment(-1, len(self.text))
                    self.draw()
                if event.key == pygame.K_RIGHT:
                    self.cursor.increment(1, len(self.text))
                    self.draw()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.set_cursor(event.pos)

    def get_rect(self):
        """Return the text input box rect."""
        line_height = self.cursor.size[1]
        line_count = max(len(self.text) // self.max_line_chars + 1, self.cursor.line + 1)
        position = (self.position[0], self.position[1] - line_height * (line_count - 1))
        size = (self.size[0], line_height * line_count)
        return pygame.Rect(position, size)

    def draw(self):
        """Draw the text input box."""
        if self.state > 0:
            lines = textwrap.wrap(self.text, self.max_line_chars)
            line_height = self.cursor.size[1]

            # Calculate the position and size of the background
            rect = self.get_rect()
            self.renderer.draw_background(self.surface, (rect.x, rect.y), rect.size)

            # Draw the lines
            i = 0
            for line in lines:
                x, y = rect.x + self.text_margin, rect.y + self.text_margin + i * line_height
                self.renderer.draw_text(self.surface, (x, y), line)
                i += 1

            # Draw the cursor
            if self.cursor.line_index > 0:
                cursor_x = self.renderer.get_text_width(lines[self.cursor.line][:self.cursor.line_index])
            else:
                cursor_x = 0
            cursor_position = (rect.x + cursor_x, rect.y + self.cursor.line * line_height)
            self.renderer.draw_cursor(self.surface, cursor_position, self.cursor)

    def add_at_cursor(self, letter):
        """Add a character whereever the cursor is currently located.

        Parameters
        ----------
        letter:
            Single char to append.
        """
        if self.cursor.index < len(self.text):
            # Inserting in the text
            self.text = self.text[:self.cursor.index] + letter + self.text[self.cursor.index:]
            self.cursor.increment(1, len(self.text))
        else:
            self.text += letter
            self.cursor.increment(1, len(self.text))
        self.draw()

    def backspace(self):
        """Delete a character before the cursor position."""
        if self.cursor.index == 0:
            return
        self.text = self.text[:self.cursor.index-1] + self.text[self.cursor.index:]
        self.cursor.increment(-1, len(self.text))
        self.draw()

    def set_text(self, text):
        """Set the current text.

        Parameters
        ----------
        text:
            New text.
        """
        self.text = text
        self.cursor.set_index(len(text))

    def set_cursor(self, position):
        """Move cursor to char nearest position (x, y).

        Parameters
        ----------
        position:
            Absolute position (x, y) on the surface.
        """
        rect = self.get_rect()
        if position[1] < rect.top or position[1] > rect.bottom:
            return

        line_height = self.cursor.size[1]
        line = int((position[1] - rect.top) / line_height)
        text = textwrap.wrap(self.text, self.max_line_chars)[line]
        text_length = len(text)

        pos = 1
        while pos < text_length:
            width = self.renderer.get_text_width(text[:pos])
            if width >= position[0] - rect.left:
                break  # we found it
            pos += 1
        self.cursor.set_index(pos, line)
        self.draw()
