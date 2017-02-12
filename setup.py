#!/usr/bin/python

from distutils.core import setup

setup(
    name = 'pygame_vkeyboard',
    packages = ['pygame_vkeyboard'], # this must be the same as the name above
    version = '1.1',
    description = 'Visual keyboard for Pygame engine. Aims to be easy to use as highly customizable as well.',
    author = 'Felix Voituret',
    author_email = 'felix.voituret@gmail.com',
    url = 'https://github.com/Faylixe/pygame_vkeyboard',
    download_url = 'https://github.com/Faylixe/pygame_vkeyboard/tarball/1.1',
    install_requires=[
        'pygame',
    ],
    keywords = ['pygame', 'keyboard'],
    classifiers = [
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: pygame'
    ],
    include_package_data=True
)