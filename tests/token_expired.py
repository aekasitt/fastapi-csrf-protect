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

def test_token_expired(setup, route: str='/protected', delay: int = 2):
  client: TestClient = setup
  
  ### Loads Config ###
  @CsrfProtect.load_config
  def get_configs():
    return [('secret_key', 'secret'), ('max_age', delay)]

  ### Get ###
  response   = client.get('/set-cookie')

  ### Assertion ###
  assert response.status_code == 200

  ### Get ###
  response = client.get(route, cookies=response.cookies)

  ### Assertions ###
  assert response.status_code == 200
  assert response.json() == {'detail': 'OK'}

  ### Delays ###
  sleep(delay)

  ### Get ###
  response = client.get(route, cookies=response.cookies)

  ### Assertions ###
  assert response.status_code == 400
  assert response.json() == {'detail': 'Missing Cookie fastapi-csrf-token'}
