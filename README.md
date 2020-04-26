# pygame-vkeyboard

[![Python package](https://github.com/Faylixe/pygame_vkeyboard/workflows/Python%20package/badge.svg?branch=master)](https://github.com/Faylixe/pygame_vkeyboard/actions) [![PyPI version](https://badge.fury.io/py/pygame-vkeyboard.svg)](https://badge.fury.io/py/pygame-vkeyboard)

Visual keyboard for Pygame engine. Aims to be easy to use as highly customizable as well.

<div align="center">
    <img
      src="https://raw.githubusercontent.com/Faylixe/pygame_vkeyboard/master/screenshot/embedded.png"
      width="80%">
    <p>Vitual keyboard with AZERTY layout</p>
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
keyboard.enable()
```

## Event managment

A ``VKeyboard`` object handles the following pygame event :

- **MOUSEBUTTONDOWN**
- **MOUSEBUTTONUP**
- **KEYDOWN**
- **KEYUP**

In order to process those events, keyboard instance event handling method should be called like in the following example:

```python
for event in pygame.event.get():
   keyboard.on_event(event)
   # Perform your other event handling here.
```

It will update key state accordingly as the keyboard buffer as well. Buffer modification will be notified
through the keyboard text consumer function.

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
A ``VKeyboardRenderer`` can be built using following constructor :

```python
renderer = VKeyboardRenderer(
    # Key font.
    pygame.font.SysFont('arial', 20),
    # Keyboard background color.
    (50, 50, 50),
    # Key background color (one per state, 0 for released, 1 for pressed).
    ((255, 255, 255), (0, 0, 0)),
    # Text color for key (one per state as for the key background).
    ((0, 0, 0), (255, 255, 255)),
    # (Optional) special key background color.
    ((255, 255, 255), (0, 0, 0)),
)
```

Please note that the default renderer implementation require a unicode font.

You can also create your own renderer. Just override ``VKeyboardRenderer``class and override any of the following methods :

- **draw_background(surface)**: Draws the background of the keyboard.
- **draw_character_key(surface, key, special=False)**: Draws a key based on character value.
- **draw_space_key(surface, key)**: Draws space bar.
- **draw_back_key(surface, key)**: Draws back key.
- **draw_uppercase_key(surface, key)**: Draw uppercase switch key.
- **draw_special_char_key(surface, key)**: Draw special character switch key.

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
