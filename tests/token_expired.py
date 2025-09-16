#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/tests/token_expired.py
# VERSION:     1.0.7
# CREATED:     2020-11-26 16:14
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from time import sleep
from typing import Union

### Third-party packages ###
from fastapi.testclient import TestClient

### Local modules ###
from fastapi_csrf_protect import CsrfProtect
from tests import test_client


def test_validate_token_expired(test_client: TestClient, max_age: int = 2) -> None:
  ### Load config ###
  @CsrfProtect.load_config
  def _() -> tuple[tuple[str, Union[int, str]], ...]:
    return (("secret_key", "secret"), ("max_age", max_age))

  ### Generate token ###
  response = test_client.get("/gen-token")

  ### Assertion ###
  assert response.status_code == 200

  ### Extract `csrf_token` from response to be set as next request's header ###
  csrf_token: str = response.json().get("csrf_token", None)
  headers: dict[str, str] = {"X-CSRF-Token": csrf_token} if csrf_token is not None else {}

  ### Delay until expiry ###
  sleep(max_age + 1)

  ### Post to protected endpoint ###
  response = test_client.post("/protected", headers=headers)

  ### Assertions ###
  assert response.status_code == 400
  assert response.json() == {"detail": "Missing Cookie: `fastapi-csrf-token`."}
