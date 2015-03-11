from __future__ import print_function
from setuptools import setup,find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import Phurt

here = os.path.abspath(os.path.dirname(__file__))

setup(
	name='Phurt',
    version='0.1.1',
	url='',
	license='',
	author='Mike Petersen',
	description='Python HDI Utilitarian Reduction Tool',
	packages=find_packages(),
    package_data={'':['*.dat']},
    include_package_data=True
)
