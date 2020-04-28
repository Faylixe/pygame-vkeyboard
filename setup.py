#!/usr/bin/env python
# coding: utf8

""" Distribution script. """

import sys
from os.path import abspath, dirname, join
from setuptools import setup, find_packages
if sys.version_info[0] == 2:
    from io import open  # Support for encoding on Python 2.x

import pygame_vkeyboard

here = dirname(abspath(__file__))
with open(join(here, 'README.md'), 'r', encoding='utf-8') as stream:
    readme = stream.read()

setup(
    name='pygame-vkeyboard',
    version=pygame_vkeyboard.__version__,
    description=pygame_vkeyboard.__doc__.split()[0],
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Felix Voituret, Antoine Rousseaux',
    author_email='felix@voituret.fr, anxuae-prog@yahoo.fr',
    url='https://github.com/Faylixe/pygame-vkeyboard',
    download_url='https://pypi.org/project/pygame-vkeyboard/#files',
    license='Apache License 2.0',
    keywords=['pygame', 'keyboard'],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: pygame'
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=2.7',
    install_requires=[
        'pygame',
    ],
    setup_requires=[
        'setuptools>=41.0.1',
        'wheel>=0.33.4'
    ],
    options={
        'bdist_wheel':
            {'universal': True}  # Support Python 2.x
    },
)
