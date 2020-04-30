#!/usr/bin/env python
# coding: utf8

"""
Text box to display the current text. The mouse events are
supported to move the cursor at the desired place.
"""

import pygame  # pylint: disable=import-error

from .vrenderers import VKeyboardRenderer


class VBackground(pygame.sprite.DirtySprite):
    """Background of the text input box. It is used to create
    borders by making its size a litle bit larger than the
    lines width and the sum of lines heights.
    """

    def __init__(self, size, renderer):
        """Default constructor.

        Parameters
        ----------
        size:
            Size tuple (width, height) of the background.
        renderer:
            Renderer used to draw the background.
        """
        super(VBackground, self).__init__()
        self.renderer = renderer
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.rect = pygame.Rect((0, 0), size)

        self.renderer.draw_background(self.image)

    def set_rect(self, x, y, width, height):
        """Set the background absolute position and size.

        Parameters
        ----------
        x:
            Position x.
        y:
            Position y.
        width:
            Background width.
        height:
            Background height.
        """
        if self.rect.topleft != (x, y):
            self.rect.topleft = (x, y)
            self.dirty = 1
        if self.rect.size != (width, height):
            self.rect.size = (width, height)
            self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            self.renderer.draw_background(self.image)
            self.dirty = 1


class VCursor(pygame.sprite.DirtySprite):
    """Handles the cursor.

    The ``index`` represente the absolute position which is the number
    of characters before it, all lines included.
    """

    def __init__(self, size, renderer):
        """Default constructor.

        Parameters
        ----------
        size:
            Size tuple (width, height) of the cursor.
        renderer:
            Renderer used to draw the cursor.
        """
        super(VCursor, self).__init__()
        self.renderer = renderer
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.index = 0
        self.selected = 0

        # Blink management
        self.clock = pygame.time.Clock()
        self.switch_ms = 400
        self.switch_counter = 0

        self.renderer.draw_cursor(self.image, self)

    def set_position(self, position):
        """Set the cursor absolute position.

        Parameters
        ----------
        position:
            Position tuple (x, y).
        """
        if self.rect.topleft != position:
            self.rect.topleft = position
            self.dirty = 1

    def set_index(self, index):
        """Move the cursor at the given index.

        Parameters
        ----------
        index:
            Absolute (sum all lines) cursor index.
        """
        if index != self.index:
            self.index = index
            self.dirty = 1

    def update(self, events):
        """Toggle visibility of the cursor."""
        self.clock.tick()
        self.switch_counter += self.clock.get_time()
        if self.switch_counter >= self.switch_ms:
            self.switch_counter %= self.switch_ms
            self.visible = int(not self.visible)
            self.dirty = 1


class VLine(pygame.sprite.DirtySprite):
    """Handles a line of text. A line can be fed until the text
    width reaches the line width.

    By default, when the line is empty, its ``visible`` attribute
    is set to 0 to hide the line.
    """

    def __init__(self, size, renderer, always_visible=False):
        """Default constructor.

        Parameters
        ----------
        size:
            Size tuple (width, height) of the line.
        renderer:
            Renderer used to draw the line.
        always_visible:
            If True, the line will be never hidden even if it is empty.
        """
        super(VLine, self).__init__()
        self.renderer = renderer
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.rect = pygame.Rect((0, 0), size)
        self.text = ''
        self.full = False
        self.always_visible = always_visible

        self.renderer.draw_text(self.image, '')

    def __len__(self):
        """Return the number of characters in the line."""
        return len(self.text)

    def set_position(self, position):
        """Set the line absolute position.

        Parameters
        ----------
        position:
            Position tuple (x, y).
        """
        if self.rect.topleft != position:
            self.rect.topleft = position
            self.dirty = 1

    def clear(self):
        """Clear the current text."""
        if self.text:
            self.text = ''
            self.full = False
            self.renderer.draw_text(self.image, '')
            if not self.always_visible:
                self.visible = 0
            else:
                self.dirty = 1
        return self.text

    def feed(self, text):
        """Feed the line with the given text. The current text is
        cleared if an empty string is given.

        Parameters
        ----------
        text:
            Text to feed in.

        Returns
        -------
        remain:
            Return the remaining text if the line is full.
        """
        if not text:
            return self.clear()
        elif self.text:
            if text.startswith(self.text):
                if self.full:
                    return text[len(self.text):]
            else:
                self.text = ''

        self.text, _ = self.renderer.truncate(text,
                                              self.rect.width,
                                              len(self.text))
        if text[len(self.text):]:
            self.full = True
        else:
            self.full = False
        self.dirty = 1
        self.visible = 1  # Show line
        self.renderer.draw_text(self.image, self.text)
        return text[len(self.text):]


class VTextInput(object):
    """Handles the text input box.
    """

    def __init__(self,
                 position,
                 size,
                 border=2,
                 renderer=VKeyboardRenderer.DEFAULT):
        """Default constructor.

        Parameters
        ----------
        position:
            Position tuple (x, y)
        size:
            Size tuple (width, height) of the text input.
        border:
            Border thickness.
        renderer:
            Text input renderer instance, using VTextInputRenderer.DEFAULT
            if not specified.
        """
        self.state = 0
        self.position = position
        self.size = size  # One ligne size
        self.text = ''
        self.text_margin = border
        self.renderer = renderer

        # Define background sprites
        self.eraser = None
        self.background = VBackground(size, renderer)
        self.background.set_rect(self.position[0],
                                 self.position[1] - 2 * self.text_margin,
                                 self.size[0],
                                 self.size[1] + 2 * self.text_margin)
        self.sprites = pygame.sprite.LayeredDirty(self.background)

        # Initialize first line
        line = VLine((self.size[0] - 2 * self.text_margin,
                      self.size[1]), renderer, True)
        line.set_position((
            self.position[0] + self.text_margin,
            self.position[1] - self.text_margin))
        self.sprites.add(line, layer=1)

        # Initialize cursor
        self.cursor = VCursor((2, size[1] - self.text_margin * 2), renderer)
        self.cursor.set_position((
            self.position[0] + self.text_margin,
            self.position[1]))
        self.sprites.add(self.cursor, layer=2)

        self.disable()

    def enable(self):
        """Set this text input as active."""
        self.state = 1
        self.cursor.visible = 1
        self.background.visible = 1
        self.sprites.get_sprites_from_layer(1)[0].visible = 1

    def is_enabled(self):
        """Return True if this keyboard is active."""
        return self.state == 1

    def disable(self):
        """Set this text input as non active."""
        self.state = 0
        self.cursor.visible = 0
        self.background.visible = 0
        self.sprites.get_sprites_from_layer(1)[0].visible = 0

    def get_rect(self):
        """Return text input rect."""
        return self.background.rect

    def draw(self, surface, force):
        """Draw the text input box.

        Parameters
        ----------
        surface:
            Surface on which the VTextInput is drawn.
        force:
            Force the drawing of the entire surface (time consuming).
        """
        # Setup the surface used to hide/clear the text input
        if surface and surface != self.eraser:
            self.eraser = surface
            self.sprites.clear(surface, self.eraser.copy())
            self.sprites.set_clip(pygame.Rect(self.position[0], 0,
                                              self.size[0],
                                              self.position[1] + self.size[1]))

        if force:
            self.sprites.repaint_rect(self.background.rect)
        return self.sprites.draw(surface)

    def update(self, events):
        """Pygame events processing callback method.

        Parameters
        ----------
        events:
            List of events to process.
        """
        if self.state > 0:
            self.sprites.update(events)
            for event in events:
                if event.type == pygame.KEYUP and self.cursor.selected:
                    if event.key == pygame.K_LEFT:
                        self.increment_cursor(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.increment_cursor(1)
                    elif event.key == pygame.K_HOME:
                        self.cursor.index = 0
                        self.increment_cursor(0)
                    elif event.key == pygame.K_END:
                        self.cursor.index = 0
                        self.increment_cursor(len(self.text))
                if event.type == pygame.MOUSEBUTTONDOWN\
                        and event.button in (1, 2, 3):
                    # Don't consider the mouse wheel (button 4 & 5):
                    self.set_cursor(event.pos)

    def update_lines(self):
        """Update lines content with the current text."""
        if self.state > 0:
            remain = self.text

            # Update existing line with text
            for line in self.sprites.get_sprites_from_layer(1):
                remain = line.feed(remain)

            # Create new lines if necessary
            while remain:
                line = VLine((self.size[0] - 2 * self.text_margin,
                              self.size[1]), self.renderer)
                self.sprites.add(line, layer=1)
                remain = line.feed(remain)

            # Update lines positions
            i = 0
            for line in reversed(self.sprites.get_sprites_from_layer(1)):
                if line.visible:
                    x = self.position[0] + self.text_margin
                    y = self.position[1] - i * self.size[1] - self.text_margin
                    line.set_position((x, y))
                    i += 1

            self.background.set_rect(self.position[0],
                                     line.rect.y - self.text_margin,
                                     self.size[0],
                                     i * self.size[1] + 2 * self.text_margin)

    def set_text(self, text):
        """Overwrite the current text with the given one. The cursor is
        moved at the end of the text.

        Parameters
        ----------
        text:
            New text.
        """
        self.text = text
        self.update_lines()
        self.cursor.index = 0
        self.increment_cursor(len(text))

    def add_at_cursor(self, text):
        """Add a text whereever the cursor is currently located.

        Parameters
        ----------
        text:
            Single char or text to append.
        """
        if self.cursor.index < len(self.text):
            # Inserting in the text
            prefix = self.text[:self.cursor.index]
            suffix = self.text[self.cursor.index:]
            self.text = prefix + text + suffix
        else:
            self.text += text
        self.update_lines()
        self.increment_cursor(1)

    def delete_at_cursor(self):
        """Delete a character before the cursor position."""
        if self.cursor.index == 0:
            return
        prefix = self.text[:self.cursor.index - 1]
        suffix = self.text[self.cursor.index:]
        self.text = prefix + suffix
        self.update_lines()
        self.increment_cursor(-1)

    def increment_cursor(self, step):
        """Move the cursor of one or more steps (but not beyond the
        text length).

        Parameters
        ----------
        step:
            From how many characters the cursor shall move.
        """
        pos = max(0, self.cursor.index + step)
        self.cursor.set_index(min(pos, len(self.text)))

        # Update cursor position
        chars_counter = 0
        for line in self.sprites.get_sprites_from_layer(1):
            if chars_counter + len(line) >= self.cursor.index:
                idx = self.cursor.index - chars_counter
                x = self.text_margin + self.renderer.get_text_width(
                    line.text[:idx])
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
        for collide in self.sprites.get_sprites_at(position):
            if isinstance(collide, VLine):
                text, width = self.renderer.truncate(
                    collide.text,
                    position[0] - collide.rect.left,
                    nearest=True)
                self.cursor.set_position((
                    width + self.text_margin,
                    collide.rect.y + self.text_margin))
                chars_counter = 0
                for line in self.sprites.get_sprites_from_layer(1):
                    if line == collide:
                        self.cursor.set_index(chars_counter + len(text))
                        return
                    chars_counter += len(line)
