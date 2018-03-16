# !/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import re

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'cards'
DESCRIPTION = 'Project task tracking / todo list.'
URL = 'https://github.com/okken/cards'
EMAIL = 'brian@pythontesting.net'
AUTHOR = 'Brian Okken'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.1.4'

REQUIRED = [ 'Click==6.7', 'tinydb==3.8.0', 'attrs==17.4.0' ]

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

def read(*parts):
    with io.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name=NAME,
    version=find_version('cards', '__init__.py'),
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    entry_points={
        'console_scripts': ['cards=cards.cli:cards_cli'],
    },
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
