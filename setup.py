#!/usr/bin/env python
# coding: utf8

""" Distribution script. """
from os.path import abspath, dirname, join
from setuptools import setup, find_packages

import src

here = abspath(dirname(__file__))
with open(join(here, 'README.md'), 'r', encoding='utf-8') as stream:
    readme = stream.read()

setup(
    name='pygame-vkeyboard',
    version=src.__version__,
    description='Visual keyboard for Pygame',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Felix Voituret',
    author_email='felix@voituret.fr',
    url='https://github.com/Faylixe/pygame-vkeyboard',
    download_url='https://pypi.org/project/pygame-vkeyboard/#files',
    license='Apache License 2.0',
    keywords=['pygame', 'keyboard'],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: pygame'
    ],
    packages=[
        'pygame.vkeyboard',
        'pygame.vkeyboard.examples'
    ],
    package_dir={
        'pygame.vkeyboard': 'src'
    },
    include_package_data=True,
    python_requires='>=2.7',
    install_requires=[
        'pygame',
    ],
    setup_requires=[
        'setuptools>=41.0.1',
        'wheel>=0.33.4'
    ]
)
