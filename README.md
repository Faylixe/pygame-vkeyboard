# pygame.vkeyboard

Visual keyboard for Pygame engine. Aims to be easy to use as highly customizable as well.

## Basic usage 

VKeyboard only require a pygame surface to be displayed on and a text consumer function, as in the following example :

```python
from pygame_vkeyboard import VKeyboard

# Initializes your window object or surface your want
# vkeyboard to be displayed on top of.
window = ... 

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

A VKeyboard handle the following pygame event :

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

Comming soon.

## Custom rendering using VKeyboardRenderer

Comming soon.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
