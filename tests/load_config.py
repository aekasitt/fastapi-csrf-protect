#!/usr/bin/env python3
# Copyright (C) 2019-2020 All rights reserved.
# FILENAME:  load_config.py
# VERSION: 	 0.1.9
# CREATED: 	 2020-11-26 16:14
# AUTHOR: 	 Aekasitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
import unittest
from fastapi_csrf_protect import CsrfProtect
from tests.base import BaseTestCase
from pydantic import ValidationError

class LoadConfigTestCase(BaseTestCase):
  def test_missing_secret_key(self, route='/protected'):
    error_called = False
    try:
      @CsrfProtect.load_config
      def load_secret_key():
        return [('secret_key', None)]
      resp = self.client.get(route)
    except Exception as err:
      error_called = True
      assert isinstance(err, RuntimeError)
      assert err.args[0] == 'A secret key is required to use CSRF.'
    assert error_called == True

  def test_load_config(self, config_key:str='secret_key', config_value='', invalid=False):
    error_called = False
    try:
      @CsrfProtect.load_config
      def load_csrf_conifig():
        return [(config_key, config_value)]
    except Exception as err:
      error_called = True
      assert isinstance(err, ValidationError)
    if invalid: assert error_called is True
    else: assert error_called is False

  def test_load_secret_key_as_int(self):
    self.test_load_config(config_key='secret_key', config_value=2, invalid=True)

  def test_load_secret_key_as_float(self):
    self.test_load_config(config_key='secret_key', config_value=1.0, invalid=True)

  def test_load_secret_key_as_bool(self):
    self.test_load_config(config_key='secret_key', config_value=True, invalid=True)

  def test_load_secret_key_as_bytes(self):
    self.test_load_config(config_key='secret_key', config_value=b'secret', invalid=True)

  def test_load_secret_key_as_str(self):
    self.test_load_config(config_key='secret_key', config_value='secret', invalid=False)

  def test_load_secret_key_as_list(self):
    self.test_load_config(config_key='secret_key', config_value=[], invalid=True)

  def test_load_secret_key_as_dict(self):
    self.test_load_config(config_key='secret_key', config_value={}, invalid=True)

  def test_load_csrf_header_name_as_int(self):
    self.test_load_config(config_key='csrf_header_name', config_value=2, invalid=True)

  def test_load_csrf_header_name_as_float(self):
    self.test_load_config(config_key='csrf_header_name', config_value=1.0, invalid=True)

  def test_load_csrf_header_name_as_bool(self):
    self.test_load_config(config_key='csrf_header_name', config_value=bool, invalid=True)

  def test_load_csrf_header_name_as_bytes(self):
    self.test_load_config(config_key='csrf_header_name', config_value=b'secret', invalid=True)
  
  def test_load_csrf_header_name_as_str(self):
    self.test_load_config(config_key='csrf_header_name', config_value='secret', invalid=False)

  def test_load_csrf_header_name_as_list(self):
    self.test_load_config(config_key='csrf_header_name', config_value=[], invalid=True)

  def test_load_csrf_header_name_as_dict(self):
    self.test_load_config(config_key='csrf_header_name', config_value={}, invalid=True)

  def test_load_csrf_header_type_as_int(self):
    self.test_load_config(config_key='csrf_header_type', config_value=2, invalid=True)

  def test_load_csrf_header_type_as_float(self):
    self.test_load_config(config_key='csrf_header_type', config_value=1.0, invalid=True)

  def test_load_csrf_header_type_as_bool(self):
    self.test_load_config(config_key='csrf_header_type', config_value=True, invalid=True)

  def test_load_csrf_header_type_as_bytes(self):
    self.test_load_config(config_key='csrf_header_type', config_value=b'secret', invalid=True)

  def test_load_csrf_header_type_as_str(self):
    self.test_load_config(config_key='csrf_header_type', config_value='secret', invalid=False)

  def test_load_csrf_header_type_as_list(self):
    self.test_load_config(config_key='csrf_header_type', config_value=[], invalid=True)

  def test_load_csrf_header_type_as_dict(self):
    self.test_load_config(config_key='csrf_header_type', config_value={}, invalid=True)

  def test_load_csrf_in_cookies_as_int(self):
    self.test_load_config(config_key='csrf_in_cookies', config_value=2, invalid=True)

  def test_load_csrf_in_cookies_as_float(self):
    self.test_load_config(config_key='csrf_in_cookies', config_value=1.0, invalid=True)

  def test_load_csrf_in_cookies_as_bool(self):
    self.test_load_config(config_key='csrf_in_cookies', config_value=True, invalid=False)

  def test_load_csrf_in_cookies_as_bytes(self):
    self.test_load_config(config_key='csrf_in_cookies', config_value=b'secret', invalid=True)

  def test_load_csrf_in_cookies_as_str(self):
    self.test_load_config(config_key='csrf_in_cookies', config_value='secret', invalid=True)

  def test_load_csrf_in_cookies_as_list(self):
    self.test_load_config(config_key='csrf_in_cookies', config_value=[], invalid=True)

  def test_load_csrf_in_cookies_as_dict(self):
    self.test_load_config(config_key='csrf_in_cookies', config_value={}, invalid=True)

  def test_load_csrf_methods_as_int(self):
    self.test_load_config(config_key='csrf_methods', config_value=2, invalid=True)

  def test_load_csrf_methods_as_float(self):
    self.test_load_config(config_key='csrf_methods', config_value=1.0, invalid=True)

  def test_load_csrf_methods_as_bool(self):
    self.test_load_config(config_key='csrf_methods', config_value=True, invalid=True)

  def test_load_csrf_methods_as_bytes(self):
    self.test_load_config(config_key='csrf_methods', config_value=b'secret', invalid=True)

  def test_load_csrf_methods_as_str(self):
    self.test_load_config(config_key='csrf_methods', config_value='secret', invalid=True)

  def test_load_csrf_methods_as_empty_list(self):
    self.test_load_config(config_key='csrf_methods', config_value=[], invalid=False)

  def test_load_csrf_methods_as_list_int(self):
    self.test_load_config(config_key='csrf_methods', config_value=[1, 2, 3], invalid=True)

  def test_load_csrf_methods_as_tuple_int(self):
    self.test_load_config(config_key='csrf_methods', config_value=(1, 2, 3), invalid=True)

  def test_load_csrf_methods_as_set_int(self):
    self.test_load_config(config_key='csrf_methods', config_value={1, 2, 3}, invalid=True)

  def test_load_csrf_methods_as_list_str(self):
    self.test_load_config(config_key='csrf_methods', config_value=['1', '2', '3'], invalid=True)

  def test_load_csrf_methods_as_tuple_str(self):
    self.test_load_config(config_key='csrf_methods', config_value=('1', '2', '3'), invalid=True)

  def test_load_csrf_methods_as_set_str(self):
    self.test_load_config(config_key='csrf_methods', config_value={'1', '2', '3'}, invalid=True)

  def test_load_csrf_methods_as_list_valid_str(self):
    self.test_load_config(config_key='csrf_methods', config_value=['GET', 'POST', 'DELETE'], invalid=False)

  def test_load_csrf_methods_as_tuple_valid_str(self):
    self.test_load_config(config_key='csrf_methods', config_value=('GET', 'POST', 'DELETE'), invalid=False)

  def test_load_csrf_methods_as_set_valid_str(self):
    self.test_load_config(config_key='csrf_methods', config_value={'GET', 'POST', 'DELETE'}, invalid=False)

  def test_load_csrf_methods_as_dict(self):
    self.test_load_config(config_key='csrf_methods', config_value={'key': 'value'}, invalid=True)

if __name__ == '__main__':
  unittest.main()