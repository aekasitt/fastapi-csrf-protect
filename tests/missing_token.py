#!/usr/bin/env python3
# Copyright (C) 2019-2020 All rights reserved.
# FILENAME:  missing_token.py
# VERSION: 	 0.2.2
# CREATED: 	 2020-11-26 16:14
# AUTHOR: 	 Aekasitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Third-Party Packages ###
from fastapi.testclient import TestClient
### Local Packages ###
from . import *
from fastapi_csrf_protect import CsrfProtect

def validate_missing_token_request(client: TestClient, route: str, expected_status: int, expected_msg: str):

  ### Loads Config ###
  @CsrfProtect.load_config
  def get_secret_key():
    return [('secret_key', 'secret')]

  ### Get ###
  response           = client.get(route)

  ### Assertions ###
  assert response.status_code == expected_status
  assert response.json()      == {'detail': expected_msg }

def test_missing_token_request_in_cookies(setup_cookies, route: str = '/protected'):
  validate_missing_token_request(setup_cookies, route, 400, 'Missing Cookie fastapi-csrf-token')

def test_missing_token_request_in_context(setup_context, route: str = '/protected'):
  validate_missing_token_request(setup_context, route, 422, 'Bad headers. Expected "X-CSRF-Token" in headers')
