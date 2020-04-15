#!/usr/bin/env python
# coding: utf8

""" Distribution script. """

from distutils.core import setup

setup(
    name='pygame_vkeyboard',
    packages=['pygame_vkeyboard'],
    version='2.0.0',
    description='''
        Visual keyboard for Pygame engine. Aims to be easy to use as
        highly customizable as well.
    ''',
    author='Felix Voituret',
    author_email='felix.voituret@gmail.com',
    url='https://github.com/Faylixe/pygame_vkeyboard',
    download_url='https://github.com/Faylixe/pygame_vkeyboard/tarball/1.1',
    install_requires=[
        'pygame',
    ],
    keywords=['pygame', 'keyboard'],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: pygame'
    ],
    include_package_data=True
)