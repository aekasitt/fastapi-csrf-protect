#!/usr/bin/env python3
# Copyright (C) 2019-2020 All rights reserved.
# FILENAME:  token_invalid.py
# VERSION: 	 0.1.6
# CREATED: 	 2020-11-26 16:14
# AUTHOR: 	 Aekasitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
import unittest
from fastapi_csrf_protect import CsrfProtect
from tests.base import BaseTestCase

class TokenInvalidTestCase(BaseTestCase):
  def test_token_invalid_request(self, route='/protected'):
    @CsrfProtect.load_config
    def get_configs():
      return [('secret_key', 'secret'), ('cookie-key', 'fastapi-csrf-token')]
    response = self.client.get('/set-cookie')
    assert response.status_code == 200
    response = self.client.get(route, cookies={ 'fastapi-csrf-token': 'invalid' })
    assert response.status_code == 401
    assert response.json() == {'detail': 'The CSRF token is invalid.'}

if __name__ == '__main__':
  unittest.main()