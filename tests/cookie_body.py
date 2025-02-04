#!/usr/bin/env python3
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/tests/cookie_body.py
# VERSION:     1.0.0
# CREATED:     2023-06-18 15:07
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Dict, Optional

### Third-party packages ###
from fastapi.testclient import TestClient

### Local modules ###
from . import test_client
from fastapi_csrf_protect import CsrfProtect


def test_submit_csrf_token_in_body_and_cookies(test_client: TestClient):
  ### Load config ###
  @CsrfProtect.load_config
  def get_configs():
    return [("secret_key", "secret"), ("token_key", "csrf-token"), ("token_location", "body")]

  ### Generate token ###
  response = test_client.get("/gen-token")
  assert response.status_code == 200

  ### Asserts that `cookie_token` is present
  cookie_token: Optional[str] = test_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is not None

  ### Extract `csrf_token` from response to be set as next request's body ###
  csrf_token: Optional[str] = response.json().get("csrf_token", None)
  payload: Dict[str, str] = {"csrf-token": csrf_token} if csrf_token is not None else {}

  ### Post to protected endpoint ###
  response = test_client.post("/protected", data=payload)

  ### Assertions ###
  assert response.status_code == 200
  assert response.json() == {"detail": "OK"}
  cookie_token = test_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is None

  ### Immediately get protected contents again ###
  response = test_client.post("/protected", data=payload)

  ### Assertions ###
  assert response.status_code == 400
  assert response.json() == {"detail": "Missing Cookie: `fastapi-csrf-token`."}


def test_submit_csrf_token_in_body_and_cookies_with_lax_cookie_samesite(test_client: TestClient):
  ### Load config ###
  @CsrfProtect.load_config
  def get_configs():
    return [
      ("cookie_samesite", "lax"),
      ("secret_key", "secret"),
      ("token_key", "csrf-token"),
      ("token_location", "body"),
    ]

  ### Generate token ###
  response = test_client.get("/gen-token")
  assert response.status_code == 200

  ### Asserts that `cookie_token` is present
  cookie_token: Optional[str] = test_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is not None

  ### Extract `csrf_token` from response to be set as next request's body ###
  csrf_token: Optional[str] = response.json().get("csrf_token", None)
  payload: Dict[str, str] = {"csrf-token": csrf_token} if csrf_token is not None else {}

  ### Post to protected endpoint ###
  response = test_client.post("/protected", data=payload)

  ### Assertions ###
  assert response.status_code == 200
  assert response.json() == {"detail": "OK"}
  cookie_token = test_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is None

  ### Immediately get protected contents again ###
  response = test_client.post("/protected", data=payload)

  ### Assertions ###
  assert response.status_code == 400
  assert response.json() == {"detail": "Missing Cookie: `fastapi-csrf-token`."}


def test_submit_csrf_token_in_body_and_cookies_with_strict_cookie_samesite(test_client: TestClient):
  ### Load config ###
  @CsrfProtect.load_config
  def get_configs():
    return [
      ("cookie_samesite", "strict"),
      ("secret_key", "secret"),
      ("token_key", "csrf-token"),
      ("token_location", "body"),
    ]

  ### Generate token ###
  response = test_client.get("/gen-token")
  assert response.status_code == 200

  ### Asserts that `cookie_token` is present
  cookie_token: Optional[str] = test_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is not None

  ### Extract `csrf_token` from response to be set as next request's body ###
  csrf_token: Optional[str] = response.json().get("csrf_token", None)
  payload: Dict[str, str] = {"csrf-token": csrf_token} if csrf_token is not None else {}

  ### Post to protected endpoint ###
  response = test_client.post("/protected", data=payload)

  ### Assertions ###
  assert response.status_code == 200
  assert response.json() == {"detail": "OK"}
  cookie_token = test_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is None

  ### Immediately get protected contents again ###
  response = test_client.post("/protected", data=payload)

  ### Assertions ###
  assert response.status_code == 400
  assert response.json() == {"detail": "Missing Cookie: `fastapi-csrf-token`."}
