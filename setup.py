#!/usr/bin/env python3
# Copyright (C) 2019-2020 All rights reserved.
# FILENAME:  setup.py
# VERSION: 	 0.0.1
# CREATED: 	 2020-11-25 14:35
# AUTHOR: 	 Aekasitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
from setuptools import setup

# Load Long Description from README
long_description = ''
with open('README.md', 'r') as readme:
  long_description = readme.read()

setup(
  name='fastapi-csrf-protect',
  version='0.1.0',
  description='Simple integration of Cross-Site Request Forgery (XSRF) Protection by using either Cookies or Context combined with Headers',
  py_modules=['fastapi_csrf_protect'],
  package_dir={'': 'fastapi_csrf_protect'},
  classifiers=[
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Operating System :: OS Independent',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ],
  long_description=long_description,
  long_description_content_type='text/markdown',
  install_requires=[
    'fastapi ~= 0.61.2',
    'itsdangerous ~= 1.1.0',
    'pydantic ~= 1.7.2',
    'requests ~= 2.25.0'
  ],
  test_suite='tests',
)