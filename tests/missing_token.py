#!/usr/bin/env python3
# Copyright (C) 2019-2020 All rights reserved.
# FILENAME:  missing_token.py
# VERSION: 	 0.1.0
# CREATED: 	 2020-11-26 16:14
# AUTHOR: 	 Aekasitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
import unittest
from fastapi_csrf import CsrfProtect
from tests.base import BaseTestCase

class MissingTokenTestCase(BaseTestCase):
  def test_missing_token_request(self, route='/protected'):
    @CsrfProtect.load_config
    def get_secret_key():
      return [('secret_key', 'secret')]
    response = self.client.get(route)
    assert response.status_code == 400
    assert response.json() == {'detail': 'Missing Cookie fastapi-csrf-token'}

if __name__ == '__main__':
  unittest.main()