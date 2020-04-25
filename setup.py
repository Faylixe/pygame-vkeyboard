#!/usr/bin/env python
# coding: utf8

""" Distribution script. """
from os.path import abspath, dirname, join
from setuptools import setup, find_packages

import pygame_vkeyboard

here = abspath(dirname(__file__))
with open(join(here, 'README.md'), 'r') as stream:
    readme = stream.read()

setup(
    name='pygame-vkeyboard',
    version=pygame_vkeyboard.__version__,
    description=pygame_vkeyboard.__doc__,
    long_description=readme,
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
