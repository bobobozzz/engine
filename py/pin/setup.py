#!/usr/bin/env python3

import sys
try:
    from setuptools import setup,find_packages
except ImportError:
    from distutils.core import setup

import pin 

setup(name='pin',
      version='1.0',
      description='Web framework for engine',
      author='',
      author_email='',
      url='',
      py_modules=['frame'],
      packages= find_packages(),
      install_requires=['Jinja2>=2'],
      scripts=['frame.py'],
      license='GPL-v3',
      platforms='LINUX',
      )
