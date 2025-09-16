#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/tests/missing_token.py
# VERSION:     1.0.7
# CREATED:     2020-11-26 16:14
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from fastapi.testclient import TestClient
from httpx import Response

### Local packages ###
from fastapi_csrf_protect import CsrfProtect
from tests import test_client


def test_validate_missing_cookie_token_request(test_client: TestClient) -> None:
  ### Loads config ###
  @CsrfProtect.load_config
  def _() -> tuple[tuple[str, str], ...]:
    return (("secret_key", "secret"),)

  ### Generate token ###
  response: Response = test_client.get("/gen-token")
  csrf_token: str = response.json().get("csrf_token", None)
  headers: dict[str, str] = {"X-CSRF-Token": csrf_token} if csrf_token is not None else {}

  ### Clear previously received cookies ###
  test_client.cookies = None  # type: ignore

  ### Post to protected endpoint ###
  response = test_client.post("/protected", headers=headers)

  ### Assertions ###
  assert response.status_code == 400
  assert response.json() == {"detail": "Missing Cookie: `fastapi-csrf-token`."}


def test_validate_missing_header_token_request(test_client: TestClient) -> None:
  ### Loads Config ###
  @CsrfProtect.load_config
  def _() -> tuple[tuple[str, str], ...]:
    return (("secret_key", "secret"),)

  ### Get CSRF Tokens ###
  response: Response = test_client.get("/gen-token")

  ### Get protected contents ###
  response = test_client.post("/protected")

  ### Assertions ###
  assert response.status_code == 422
  assert response.json() == {"detail": 'Bad headers. Expected "X-CSRF-Token" in headers'}
