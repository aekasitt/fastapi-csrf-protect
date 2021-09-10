#!/usr/bin/env python3
# Copyright (C) 2019-2020 All rights reserved.
# FILENAME:  missing_secret.py
# VERSION: 	 0.2.0
# CREATED: 	 2021-08-18 23:58
# AUTHOR: 	 Aekasitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Third-Party Packages ###
from fastapi.testclient import TestClient
### Local Modules ###
from . import *
from fastapi_csrf_protect import CsrfProtect

def test_missing_secret_key(setup, route: str='/protected'):
  client: TestClient = setup
  error_called: bool = False
  try:
    @CsrfProtect.load_config
    def load_secret_key():
      return [('secret_key', None)]
    client.get(route)
  except Exception as err:
    error_called = True
    assert isinstance(err, RuntimeError)
    assert err.args[0] == 'A secret key is required to use CSRF.'
  assert error_called == True
