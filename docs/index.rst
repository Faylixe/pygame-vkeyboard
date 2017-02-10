Usage guide for pygame_vkeyboard
============================================

Visual keyboard for Pygame engine. Aims to be easy to use as highly customizable as well.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

Basic usage 
-----------

VKeyboard only require a pygame surface to be displayed on and a text consumer function, as in the following example :

.. code-block:: python

    from pygame_vkeyboard import VKeyboard

    # Initializes your window object or surface your want
    # vkeyboard to be displayed on top of.
    window = ... 

    def consume(text):
        """ """
        print('Current text : %s' % text)

    # Initializes and activates vkeyboard
    layout = VKeyboardLayout(VKeyboardLayout.AZERTY, True, True)
    keyboard = VKeyboard(window, consumer, layout)
    keyboard.enable()
    keyboard.draw()

Event managment
---------------

Comming soon.

Customize layout 
----------------

Comming soon.

Custom rendering using VKeyboardStyle
-------------------------------------

Comming soon.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
