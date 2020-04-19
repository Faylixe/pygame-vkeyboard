#!/usr/bin/env python
# coding: utf8

""" Distribution script. """

import os
import sys
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, HERE)  # To be able to import the package
import pygame_vkeyboard


setup(
    name='pygame-vkeyboard',
    version=pygame_vkeyboard.__version__,
    description=pygame_vkeyboard.__doc__,
    long_description=open(os.path.join(HERE, 'README.md'), encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Felix Voituret',
    author_email='felix.voituret@gmail.com',
    url='https://github.com/Faylixe/pygame_vkeyboard',
    download_url='https://pypi.org/project/pygame-vkeyboard/#files',
    license='Apache License 2.0',
    keywords=['pygame', 'keyboard'],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: pygame'
    ],
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    python_requires='>=2.7',
    install_requires=[
        'pygame',
    ],
    setup_requires=[
        'setuptools>=38.6.0',
        'wheel>=0.31.0'
    ],
    options={
        'bdist_wheel':
            {'universal': True}
    },
)
