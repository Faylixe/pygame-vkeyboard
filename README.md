# pygame.vkeyboard

Visual keyboard for Pygame engine. Aims to be easy to use as highly customizable as well.

# Basic usage 

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
keyboard = VKeyboard(window, consumer)
keyboard.active = True
keyboard.draw()
```

More features can be found, by reading the docs.