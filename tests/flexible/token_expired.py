#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/tests/flexible/token_expired.py
# VERSION:     1.0.7
# CREATED:     2025-08-18 08:53:00+02:00
# AUTHOR:      Eliam Lotonga <e.m.lotonga@gmail.com>
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
from fastapi_csrf_protect.flexible import CsrfProtect
from tests.flexible import flexible_client


def test_validate_token_expired(flexible_client: TestClient, max_age: int = 2) -> None:
  ### Load config ###
  @CsrfProtect.load_config
  def _() -> tuple[tuple[str, Union[int, str]], ...]:
    return (("secret_key", "secret"), ("max_age", max_age))

  ### Generate token ###
  response = flexible_client.get("/gen-token")

  ### Assertion ###
  assert response.status_code == 200

  ### Extract `csrf_token` from response to be set as next request's header ###
  csrf_token: str = response.json().get("csrf_token", None)
  headers: dict[str, str] = {"X-CSRF-Token": csrf_token} if csrf_token is not None else {}

  ### Delay until expiry ###
  sleep(max_age + 1)

  ### Post to protected endpoint ###
  response = flexible_client.post("/protected", headers=headers)

  ### Assertions ###
  assert response.status_code == 400
  assert response.json() == {"detail": "Missing Cookie: `fastapi-csrf-token`."}
