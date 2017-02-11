# pygame_vkeyboard

Visual keyboard for Pygame engine. Aims to be easy to use as highly customizable as well.

## Basic usage 

``VKeyboard`` only require a pygame surface to be displayed on and a text consumer function, as in the following example :

```python
from pygame_vkeyboard import *

# Initializes your window object or surface your want
# vkeyboard to be displayed on top of.
surface = ... 

def consume(text):
    """ """
    print('Current text : %s' % text)

# Initializes and activates vkeyboard
layout = VKeyboardLayout(VKeyboardLayout.AZERTY)
keyboard = VKeyboard(window, consumer, layout)
keyboard.enable()
keyboard.draw()
```

## Event managment

A ``VKeyboard`` handle the following pygame event :

- **MOUSEBUTTONDOWN**
- **MOUSEBUTTONUP**
- **KEYDOWN**
- **KEYUP**

In order to process those event, keyboard instance event handling method should be called like in the following example:

```python
for event in pygame.event.get():
   keyboard.on_event(event)
   # Perform your other event handling here.
```

It will update key state accordingly as the keyboard buffer as well. Buffer modification will be notified
through the keyboard text consumer function.

## Customize layout 

The keyboard layout is the keyboard model that indicates which key is displayed and how they are dispatched
across the keyboard space. It consists in a ``VKeyboardLayout`` object which is built using list of string
each string corresponding to a keyboard key row. ``VkeyboardLayout`` constructor is defined as following :

```python
def __init__(self, model, key_size=None, allow_uppercase=True, allow_special_chars=True)
```

If the **key_size** parameter is not provided, it will be computed dynamically regarding of the target
surface the keyboard will be rendered into.

In order to only display a numerical ``Vkeyboard`` for example, you can use a custom layout like this :

```python
model = ['123', '456', '789', '0']
layout = VKeyboardLayout(model)
````
It will dispatch


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
    # Padding in pixel between two keys.
    5
)
```

You can also create your own renderer. It simple consists in two methods :

- **drawBackground(surface, position, size)**: Draws the background of the keyboard.
- **drawKey(surface, key)**: Draws the given ``VKey`` object.