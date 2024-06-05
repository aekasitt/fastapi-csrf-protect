#!/usr/bin/env python3
# Copyright (C) 2021-2023 All rights reserved.
# FILENAME:  token_expired.py
# VERSION: 	 0.3.3
# CREATED: 	 2020-11-26 16:14
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from time import sleep

### Third-Party packages ###
from fastapi.testclient import TestClient

### Local modules ###
from . import test_client
from fastapi_csrf_protect import CsrfProtect


def test_validate_token_expired(test_client: TestClient, max_age: int = 2):
  ### Loads Config ###
  @CsrfProtect.load_config
  def get_configs():
    return [("secret_key", "secret"), ("max_age", max_age)]

  ### Generate token ###
  response = test_client.get("/gen-token")

  ### Assertion ###
  assert response.status_code == 200

  ### Extract `csrf_token` from response to be set as next request's header ###
  csrf_token: str = response.json().get("csrf_token", None)
  headers: dict = {"X-CSRF-Token": csrf_token} if csrf_token is not None else {}

  ### Delays ###
  sleep(max_age + 1)

  ### Get protected contents ###
  response = test_client.get("/protected", headers=headers)

  ### Assertions ###
  assert response.status_code == 400
  assert response.json() == {"detail": "Missing Cookie: `fastapi-csrf-token`."}
