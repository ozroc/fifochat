#!/usr/bin/env python
from setuptools import setup

# Put here required packages or
# Uncomment one or more lines below in the install_requires section
# for the specific client drivers/modules your application needs.

setup(name='fifochat', version='1.0',
      description='fifochat',
      author='Pablo Manuel García Corzo', author_email='pablo.manuel.garcia@blue-tc.com',
      url='',
      install_requires=[
        'pymongo',
        'tornado',
        'pandas'
        ],
     )
