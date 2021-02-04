#!/usr/bin/env python3

#BoBoBo#

from setuptools import setup, find_packages

setup(
    name='engine-pin',
    version='0.3.0b6',
    keywords=("framework", "WSGI", "functional", "nginx"),
    url='https://github.com/bobobozzz/engine.git',
    author='BoBoBo',
    author_email='bobobonet@163.com',
    description="A functional and WSGI compliant web framework",
    packages=find_packages(),
    install_requires=['Jinja2>=2.11.2', 'MarkupSafe>=1.1.1',
                      'pytest>=6.1.2', 'PyMySQL>=0.10.1', 'DBUtils>=2.0'],
    include_package_data=True,
    platforms="any",
    license="GPL v3.0"
)
