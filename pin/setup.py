#!/usr/bin/env python3

#BoBoBo#

import os
from setuptools import setup, find_packages

def _process_requirements():
    packages = open('requirements.txt').read().strip().split('\n')
    requires = []
    for pkg in packages:
        if pkg.startswith('git+ssh'):
            return_code = os.system('pip install {}'.format(pkg))
            assert return_code == 0, 'error, status_code is: {}, exit!'.format(return_code)
        else:
            requires.append(pkg)
    return requires

setup(
    name='pin',
    version='0.2.2',
    author='BoBoBo',
    description="A functional and WSGI compliant web framework",
    packages=find_packages(),
    install_requires=_process_requirements()
)
