#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/tests/token_reuse.py
# VERSION:     1.0.7
# CREATED:     2023-06-18 15:07
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
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
from fastapi_csrf_protect import CsrfProtect
from tests import test_client


def test_disallow_token_reuse(test_client: TestClient, max_age: int = 2) -> None:
  ### Loads config ###
  @CsrfProtect.load_config
  def _() -> list[tuple[str, Union[int, str]]]:
    return [("secret_key", "secret"), ("max_age", max_age)]

  ### Generate token ###
  response: Response = test_client.get("/gen-token")

  ### Assertion ###
  assert response.status_code == 200

  ### Extract `csrf_token` from response to be set as next request's header ###
  csrf_token: str = response.json().get("csrf_token", None)
  headers: dict[str, str] = {"X-CSRF-Token": csrf_token} if csrf_token is not None else {}

  ### Post to protected endpoint ###
  response = test_client.post("/protected", headers=headers)

  ### Assertions ###
  assert response.status_code == 200
  assert response.json() == {"detail": "OK"}

  ### Immediately get protected contents again ###
  response = test_client.post("/protected", headers=headers)

  ### Assertions ###
  assert response.status_code == 400
  assert response.json() == {"detail": "Missing Cookie: `fastapi-csrf-token`."}
