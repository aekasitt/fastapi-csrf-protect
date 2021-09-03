#!/usr/bin/env python3
# Copyright (C) 2019-2020 All rights reserved.
# FILENAME:  token_expired.py
# VERSION: 	 0.1.7
# CREATED: 	 2020-11-26 16:14
# AUTHOR: 	 Aekasitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
import unittest
from time import sleep
from fastapi_csrf_protect import CsrfProtect
from tests.base import BaseTestCase

global delay
delay = 2

class TokenExpiredTestCase(BaseTestCase):
  def test_token_expired(self, route='/protected'):
    @CsrfProtect.load_config
    def get_configs():
      return [('secret_key', 'secret'), ('max_age', delay)]
    response = self.client.get('/set-cookie')
    assert response.status_code == 200
    response = self.client.get(route, cookies=response.cookies)
    assert response.status_code == 200
    assert response.json() == {'detail': 'OK'}
    sleep(delay)
    response = self.client.get(route, cookies=response.cookies)
    assert response.status_code == 400
    assert response.json() == {'detail': 'Missing Cookie fastapi-csrf-token'}

if __name__ == '__main__':
  unittest.main()