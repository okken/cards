# !/usr/bin/env python
# -*- coding: utf-8 -*-

from io import open
from os import path
import re

from setuptools import find_packages, setup


def read(*parts):
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, *parts), 'r', encoding='utf-8') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="cards",
    version=find_version('src', 'cards', '__init__.py'),
    description='Project task tracking / todo list.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Brian Okken',
    author_email='brian@pythontesting.net',
    python_requires='>=3.6.0',
    url='https://github.com/okken/pytest-md.git',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': ['cards=cards.cli:cards_cli'],
    },
    install_requires=['click',     # for CLI
                      'tabulate',  # for CLI
                      'tinydb',    # for DB
                      "dataclasses; python_version<'3.7'"],
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
