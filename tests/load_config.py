#!/usr/bin/env python3
# Copyright (C) 2019-2020 All rights reserved.
# FILENAME:  load_config.py
# VERSION: 	 0.2.2
# CREATED: 	 2020-11-26 16:14
# AUTHOR: 	 Aekasitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from typing import Any
### Third-Party Packages ###
import pytest
from pydantic import ValidationError
### Local Modules ###
from . import *
from fastapi_csrf_protect import CsrfProtect

@pytest.mark.parametrize('config_key, config_value, valid', [
  ('header_name', 2, False), \
    ('header_name', 1.0, False), \
      ('header_name', True, False), \
        ('header_name', b'header_name', False) ,\
          ('header_name', 'header_name', True), \
            ('header_name', [], False), \
              ('header_name', {}, False), \
  ('header_type', 2, False), \
    ('header_type', 1.0, False), \
      ('header_type', True, False), \
        ('header_type', b'header_type', False) ,\
          ('header_type', 'header_type', True), \
            ('header_type', [], False), \
              ('header_type', {}, False), \
  ('methods', 2, False), \
    ('methods', 1.0, False), \
      ('methods', True, False), \
        ('methods', b'GET, POST', False) ,\
          ('methods', 'GET, POST', False), \
            ('methods', [], True), \
              ('methods', {}, False), \
                ('methods', [1, 2, 3], False), \
                  ('methods', (1, 2, 3), False), \
                    ('methods', {1, 2, 3}, False), \
                      ('methods', ['1', '2', '3'], False), \
                        ('methods', ('1', '2', '3'), False), \
                          ('methods', {'1', '2', '3'}, False), \
                            ('methods', ['GET', 'POST', 'DELETE'], True), \
                              ('methods', ('GET', 'POST', 'DELETE'), True), \
                                ('methods', {'GET', 'POST', 'DELETE'}, True), \
                                  ('methods', {'key': 'value'}, False), \
    ('secret_key', 2, False), \
      ('secret_key', 1.0, False), \
        ('secret_key', True, False), \
          ('secret_key', b'secret', False), \
            ('secret_key', 'secret', True), \
              ('secret_key', [], False), \
                ('secret_key', {}, False), \
        ])
def test_load_config(config_key:str, config_value: Any, valid: bool):
  error_raised: bool = False
  try:
    @CsrfProtect.load_config
    def load_configs():
      return [(config_key, config_value)]
  except Exception as err:
    error_raised = True
    assert isinstance(err, ValidationError)
  assert error_raised is (True, False)[valid]
