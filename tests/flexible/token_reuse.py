#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/tests/flexible/token_reuse.py
# VERSION:     1.0.7
# CREATED:     2025-08-18 08:53:00+02:00
# AUTHOR:      Eliam Lotonga <e.m.lotonga@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Union

### Third-party packages ###
from fastapi.testclient import TestClient
from httpx import Response

### Local modules ###
from fastapi_csrf_protect.flexible import CsrfProtect
from tests.flexible import flexible_client


def test_disallow_token_reuse(flexible_client: TestClient, max_age: int = 2) -> None:
  ### Loads config ###
  @CsrfProtect.load_config
  def _() -> list[tuple[str, Union[int, str]]]:
    return [("secret_key", "secret"), ("max_age", max_age)]

  ### Generate token ###
  response: Response = flexible_client.get("/gen-token")

  ### Assertion ###
  assert response.status_code == 200

  ### Extract `csrf_token` from response to be set as next request's header ###
  csrf_token: str = response.json().get("csrf_token", None)
  headers: dict[str, str] = {"X-CSRF-Token": csrf_token} if csrf_token is not None else {}

  ### Post to protected endpoint ###
  response = flexible_client.post("/protected", headers=headers)

  ### Assertions ###
  assert response.status_code == 200
  assert response.json() == {"detail": "OK"}

  ### Immediately get protected contents again ###
  response = flexible_client.post("/protected", headers=headers)

  ### Assertions ###
  assert response.status_code == 400
  assert response.json() == {"detail": "Missing Cookie: `fastapi-csrf-token`."}
