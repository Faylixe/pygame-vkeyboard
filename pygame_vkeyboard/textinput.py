# coding: utf8


import os.path as osp
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

        Parameters
        ----------
        size:
            Size of the rectangle to fit
        """
        self.font = pygame.font.Font(self.font_name, 1)

        # Ensure a large panel of characters heights
        text = "?/|!()§&@0123456789azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN"
        i = 0
        text_height = 0
        while text_height < size[1]:
            text_height = self.font.size(text)[1]
            self.font = pygame.font.Font(self.font_name, i)
            i += 1

    def draw_cursor(self, surface):
        """Default drawing method for cursor.

        Cursor is drawn as a simple rectangle filled using this
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
        surface.fill(self.background_color)
        surface.blit(self.font.render(text, 1, self.text_color), (0, 0))


# Default text renderer
pygame.font.init()
TextInputRenderer.DEFAULT = TextInputRenderer(
    osp.join(osp.dirname(__file__), 'DejaVuSans.ttf'),
    (255, 255, 255), (255, 255, 255), (255, 255, 255), (0, 0, 0))


class TextInputCursor(pygame.sprite.DirtySprite):
    """
    Handles the cursor.

    Holds cursor information (its position), as it's state, 1 for visible,
    0 for hidden. Also contains it size / position properties.

    The ``index`` represente the absolute position. The ``line_index`` is
    the position in the current line.
    """

    def __init__(self, size, renderer):
        super(TextInputCursor, self).__init__()
        self.renderer = renderer
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.renderer.draw_cursor(self.image)
        self.rect = self.image.get_rect()
        self.index = 0

        # Blink management
        self.clock = pygame.time.Clock()
        self.switch_ms = 500
        self.switch_counter = 0

    def set_position(self, position):
        if self.rect.x != position[0]:
            self.rect.x = position[0]
            self.dirty = 1
        if self.rect.y != position[1]:
            self.rect.y = position[1]
            self.dirty = 1

    def set_index(self, index):
        """Move the cursor at the given index"""
        self.index = index
        self.dirty = 1

    def toggle(self):
        """Toggle visibility of the cursor"""
        self.clock.tick()
        self.switch_counter += self.clock.get_time()
        if self.switch_counter >= self.switch_ms:
            self.switch_counter %= self.switch_ms
            self.visible = int(not self.visible)
            self.dirty = 1


class TextInputLine(pygame.sprite.DirtySprite):

    def __init__(self, size, renderer):
        super(TextInputLine, self).__init__()
        self.renderer = renderer
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.rect = pygame.Rect((0, 0), size)
        self.text = ''
        self.full = False

    def __len__(self):
        return len(self.text)

    def set_position(self, position):
        if self.rect.x != position[0]:
            self.rect.x = position[0]
            self.dirty = 1
        if self.rect.y != position[1]:
            self.rect.y = position[1]
            self.dirty = 1

    def complete_line(self, text):
        start, end = len(self.text), len(text)
        width = self.rect.width
        while start < end:
            k = (start + end) // 2
            width = self.renderer.get_text_width(text[:k+1])
            if width > self.rect.width:
                end = k
            else:
                start = k + 1

        self.text = text[:start]
        if text[start:]:
            self.full = True
        else:
            self.full = False
        self.dirty = 1
        self.visible = 1  # Show line
        self.renderer.draw_text(self.image, self.text)
        return text[start:]

    def clear(self):
        if self.text:
            self.text = ''
            self.full = False
            self.visible = 0  # Hide empty line
        return self.text

    def feed(self, text):
        if not text:
            return self.clear()
        elif not self.text:
            return self.complete_line(text)
        elif text.startswith(self.text):
            if self.full:
                return text[len(self.text):]
        else:
            self.text = ''

        return self.complete_line(text)


class TextInput(object):
    """
    Handles the text input box.
    """

    def __init__(self, position, size, renderer=TextInputRenderer.DEFAULT):
        self.state = 0
        self.position = position
        self.size = size  # One ligne size
        self.text = ''
        self.text_margin = 2

        # Make sprites
        self.background = None
        self.cursor = TextInputCursor((2, size[1] - self.text_margin * 2), renderer)
        self.sprites = pygame.sprite.LayeredDirty(self.cursor, layer=1)

        # Initialize renderer
        self.renderer = renderer
        self.renderer.fit_font((size[0] - 2 * self.text_margin, size[1] - 4))

    def enable(self):
        """Set this text input as active."""
        self.state = 1

    def disable(self):
        """Set this text input as non active."""
        self.state = 0

    def draw(self, surface):
        """Draw the text input box."""
        if self.state > 0:
            if not self.background:
                self.background = surface.copy()
                self.sprites.clear(surface, self.background)
            return self.sprites.draw(surface)

    def update(self, events):
        """Pygame event processing callback method.

        Parameters
        ----------
        events:
            Events to process.
        """
        if self.state > 0:

            self.cursor.toggle()

            for event in events:
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.move_cursor(-1)
                    if event.key == pygame.K_RIGHT:
                        self.move_cursor(1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.set_cursor(event.pos)

    def update_lines(self):
        """Update lines with the current text"""
        remain = self.text

        # Update existing line with text
        for line in self.sprites.get_sprites_from_layer(0):
            remain = line.feed(remain)

        # Create new lines if necessary
        while remain:
            line = TextInputLine((self.size[0] - 2 * self.text_margin,
                                  self.size[1]),
                                 self.renderer)
            self.sprites.add(line, layer=0)
            remain = line.feed(remain)

        # Update lines positions
        i = 0
        for line in reversed(self.sprites.get_sprites_from_layer(0)):
            if line.visible:
                x = self.position[0] + self.text_margin
                y = self.position[1] - i * (self.size[1] - 1)
                line.set_position((x, y))
                i += 1

    def add_at_cursor(self, text):
        """Add a text whereever the cursor is currently located.

        Parameters
        ----------
        text:
            Single char or text to append.
        """
        if self.cursor.index < len(self.text):
            # Inserting in the text
            self.text = self.text[:self.cursor.index] + text + self.text[self.cursor.index:]
        else:
            self.text += text
        self.update_lines()
        self.move_cursor(1)

    def backspace(self):
        """Delete a character before the cursor position."""
        if self.cursor.index == 0:
            return
        self.text = self.text[:self.cursor.index - 1] + self.text[self.cursor.index:]
        self.update_lines()
        self.move_cursor(-1)

    def move_cursor(self, step):
        """Move the cursor of one or more steps (but not beyond the text length)"""
        pos = max(0, self.cursor.index + step)
        self.cursor.set_index(min(pos, len(self.text)))

        # Update cursor position
        chars_counter = 0
        for line in self.sprites.get_sprites_from_layer(0):
            if chars_counter + len(line) >= self.cursor.index:
                idx = self.cursor.index - chars_counter
                x = self.renderer.get_text_width(line.text[:idx])
                self.cursor.set_position((x, line.rect.y + self.text_margin))
                break
            chars_counter += len(line)

    def set_cursor(self, position):
        """Move cursor to char nearest position (x, y).

        Parameters
        ----------
        position:
            Absolute position (x, y) on the surface.
        """
        lines = self.sprites.get_sprites_at(position)
        if lines:
            currline = lines[0]
            text_length = len(currline)

            pos = 1
            while pos < text_length:
                width = self.renderer.get_text_width(currline.text[:pos])
                if width >= position[0] - currline.rect.left:
                    self.cursor.set_position((width, currline.rect.y + self.text_margin))
                    break  # we found it
                pos += 1

            chars_counter = 0
            for line in self.sprites.get_sprites_from_layer(0):
                if line == currline:
                    self.cursor.set_index(chars_counter + pos)
                    break
                chars_counter += len(line)
