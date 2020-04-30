#!/usr/bin/env python
# coding: utf8

from pygame_vkeyboard.examples import azerty, numeric, textinput


def test_example_azerty():
    """Run the ASERTY example."""
    azerty.main(test=True)


def test_example_numeric():
    """Run the NUMERIC example."""
    numeric.main(test=True)


def test_example_textinput():
    """Run the TEXTINPUT example."""
    textinput.main(test=True)
