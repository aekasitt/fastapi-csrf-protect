#!/usr/bin/env python3
# Copyright (C) 2019-2020 All rights reserved.
# FILENAME:  token_expired.py
# VERSION: 	 0.2.0
# CREATED: 	 2020-11-26 16:14
# AUTHOR: 	 Aekasitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from time import sleep
### Third-Party Packages ###
from fastapi.testclient import TestClient
### Local Modules ###
from . import *
from fastapi_csrf_protect import CsrfProtect

def validate_token_expired(client: TestClient, route: str = '/set-cookie', max_age: int = 2):

  ### Loads Config ###
  @CsrfProtect.load_config
  def get_configs():
    return [('secret_key', 'secret'), ('max_age', max_age)]

  ### Get ###
  response = client.get(route)

  ### Assertion ###
  assert response.status_code == 200
  csrf_token: str = response.json().get('csrf_token', None)
  headers: dict   = { 'X-CSRF-Token': csrf_token } if csrf_token is not None else {}

  ### Get ###
  response = client.get('/protected', cookies=response.cookies, headers=headers)

  ### Assertions ###
  assert response.status_code == 200
  assert response.json() == {'detail': 'OK'}

  ### Delays ###
  sleep(max_age)

  ### Get ###
  response = client.get('/protected', cookies=response.cookies, headers=headers)

  ### Assertions ###
  assert response.status_code == 400
  assert response.json() == {'detail': 'Missing Cookie fastapi-csrf-token'}

def test_token_expired_in_cookies(setup_cookies):
  validate_token_expired(setup_cookies, '/set-cookie')

def test_token_expired_in_context(setup_context):
  validate_token_expired(setup_context, '/set-context')
