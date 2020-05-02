# pygame-vkeyboard

[![Python package](https://github.com/Faylixe/pygame_vkeyboard/workflows/Python%20package/badge.svg?branch=master)](https://github.com/Faylixe/pygame_vkeyboard/actions) [![PyPI version](https://badge.fury.io/py/pygame-vkeyboard.svg)](https://badge.fury.io/py/pygame-vkeyboard) [![PyPI downloads](https://img.shields.io/pypi/dm/pygame-vkeyboard?color=purple)](https://pypi.org/project/pibooth)

Visual keyboard for Pygame engine. Aims to be easy to use as highly customizable as well.

<div align="center">
    <table>
    <tr>
        <td><img src="https://raw.githubusercontent.com/Faylixe/pygame_vkeyboard/master/screenshot/vkeyboard_azerty.png">
        </td>
        <td><img src="https://github.com/Faylixe/pygame-vkeyboard/blob/master/screenshot/vkeyboard_numeric.gif?raw=true">
        </td>
        <td><img src="https://github.com/Faylixe/pygame-vkeyboard/blob/master/screenshot/vkeyboard_textinput.gif?raw=true">
        </td>
    </tr>
    </table>
</div>

## Install

```bash
pip install pygame-vkeyboard
```

## Basic usage

``VKeyboard`` only require a pygame surface to be displayed on and a text consumer function, as in the following example :

```python
from pygame_vkeyboard import *

# Initializes your window object or surface your want
# vkeyboard to be displayed on top of.
surface = ...

def consumer(text):
    print('Current text : %s' % text)

# Initializes and activates vkeyboard
layout = VKeyboardLayout(VKeyboardLayout.AZERTY)
keyboard = VKeyboard(surface, consumer, layout)
```

The keyboard has the following optional parameters:

- **show_text**: display a text bar with the current text
- **renderer** : define a custom renderer (see chapter below)
- **special_char_layout**: define a custom layout for special characters
- **joystick_navigation**: enable navigation using a joystick

## Event management

A ``VKeyboard`` object handles the following pygame event :

- **MOUSEBUTTONDOWN**
- **MOUSEBUTTONUP**
- **KEYDOWN**
- **KEYUP**
- **JOYHATMOTION**
- **JOYBUTTONDOWN**
- **JOYBUTTONUP**

In order to process those events, keyboard instance event handling method should be called like in the following example:

```python
while True:

    events = pygame.event.get()

    # Update internal variables
    keyboard.update(events)

    # Draw the keyboard
    keyboard.draw(surface)

    #
    # Perform other tasks here
    #

    # Update the display
    pygame.display.flip()
```

It will update key state accordingly as the keyboard buffer as well.
The buffer modification will be notified through the keyboard text consumer function.

The global performances can be improved by avoiding to flip the entire display
at each loop by using the ``pygame.display.update()`` function.

```python
while True:

    # Draw the keyboard
    rects = keyboard.draw(surface)

    # Update only the dirty rectangles of the display
    pygame.display.update(rects)
```

**Note:** the ``surface`` parameter of the ``draw()`` method is optional, it is used to clear/hide the keyboard when it is necessary and may be mandatory if the surface has changed.

## Customize layout

The keyboard layout is the model that indicates keys are displayed and how they are dispatched
across the keyboard space. It consists in a ``VKeyboardLayout`` object which is built using list of string,
each string corresponding to a keyboard key row. ``VkeyboardLayout`` constructor signature is defined as following :

```python
def __init__(self, model, key_size=None, padding=5, allow_uppercase=True, allow_special_chars=True, allow_space=True)
```

If the **key_size** parameter is not provided, it will be computed dynamically regarding of the target
surface the keyboard will be rendered into.

In order to only display a numerical ``Vkeyboard`` for example, you can use a custom layout like this :

```python
model = ['123', '456', '789', '0']
layout = VKeyboardLayout(model)
```

## Custom rendering using VKeyboardRenderer

If you want to customize keyboard rendering you could provide a ``VKeyboardRenderer`` instance at ``VKeyboard``construction.

```python
keyboard = VKeyboard(surface, consumer, layout, renderer=VKeyboardRenderer.DARK)
```

Here is the list of default renderers provided with ``pygame-vkeyboard``:

- VKeyboardRenderer.DEFAULT
- VKeyboardRenderer.DARK

A custom ``VKeyboardRenderer`` can be built using following constructor :

```python
renderer = VKeyboardRenderer(
    # Key font name/path.
    'arial',
    # Text color for key and text box (one per state: released, pressed).
    ((0, 0, 0), (255, 255, 255)),
    # Text box cursor color.
    (0, 0, 0),
    # Color to highlight the selected key.
    (20, 200, 98),
    # Keyboard background color.
    (50, 50, 50),
    # Key background color (one per state, as for the text color).
    ((255, 255, 255), (0, 0, 0)),
    # Text input background color.
    (220, 220, 220),
    # Optional special key text color (one per state, as for the text color).
    ((0, 250, 0), (255, 255, 255)),
    # Optional special key background color (one per state, as for the text color).
    ((255, 255, 255), (0, 0, 0)),
)
```

Please note that the default renderer implementation require a unicode font.

You can also create your own renderer. Just override ``VKeyboardRenderer``class and override any of the following methods :

- **draw_background(surface)**: Draws the background of the keyboard.
- **draw_text(surface, text)**: Draws the text of the text input box.
- **draw_cursor(surface, cursor)**: Draws the cursor of the text input box.
- **draw_character_key(surface, key, special=False)**: Draws a key based on character value.
- **draw_space_key(surface, key)**: Draws space bar.
- **draw_back_key(surface, key)**: Draws back key.
- **draw_uppercase_key(surface, key)**: Draw uppercase switch key.
- **draw_special_char_key(surface, key)**: Draw special character switch key.


## Getting/Setting data

Several information can be retrieved from the keyboard:

```python
keyboard = VKeyboard(...)

# Get a pygame.Rect object in which the keyboard is included.
keyboard.get_rect()

# Get the current text.
keyboard.get_text()

# Set the current text (clear the existing one).
keyboard.set_text("Hello world!")

# Return True if the keyboard is enabled (thus displayed at screen).
keyboard.is_enabled()

# Disable and hide the keyboard (keyboard.update() and keyboard.draw() have no effect).
keyboard.disable()
```

## Run examples

Several examples are provided with the **pygame_vkeyboard** library.
To run the examples, simply execute these commands in a terminal:

```bash
python -m pygame_vkeyboard.examples.azerty
python -m pygame_vkeyboard.examples.numeric
python -m pygame_vkeyboard.examples.textinput
```

## Contributing

If you develop you own renderer please share it ! I will keep a collection of rendering class in this repository.
Don't hesitate to report bug, feedback, suggestion into the repository issues section.
