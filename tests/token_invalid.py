#!/usr/bin/env python3
# Copyright (C) 2019-2020 All rights reserved.
# FILENAME:  token_invalid.py
# VERSION: 	 0.2.0
# CREATED: 	 2020-11-26 16:14
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


def validate_token_invalid_request(client: TestClient, route: str = '/set-cookie'):

  @CsrfProtect.load_config
  def get_configs():
    return [('secret_key', 'secret'), ('cookie-key', 'fastapi-csrf-token')]

  ### Get ###
  response        = client.get(route)
  csrf_token: str = response.json().get('csrf_token', None)
  headers: dict   = { 'X-CSRF-Token': csrf_token } if csrf_token is not None else {}

  ### Assertion ###
  assert response.status_code == 200

  ### Get ###
  response        = client.get('/protected', cookies={ 'fastapi-csrf-token': 'invalid' }, headers=headers)

  ### Assertions ###
  assert response.status_code == 401
  assert response.json()      == {'detail': 'The CSRF token is invalid.'}

def test_token_invalid_request_in_cookies(setup_cookies):
  validate_token_invalid_request(setup_cookies, '/set-cookie')

def test_token_invalid_request_in_context(setup_context):
  validate_token_invalid_request(setup_context, '/set-context')
