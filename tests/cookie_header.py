#!/usr/bin/env python3
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/tests/cookie_header.py
# VERSION:     1.0.0
# CREATED:     2025-02-04 11:14
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Dict, Optional, Tuple

### Third-party packages ###
from fastapi.testclient import TestClient
from pytest import mark

### Local modules ###
from . import test_client
from fastapi_csrf_protect import CsrfProtect


@mark.parametrize(
  "csrf_settings",
  (
    (("secret_key", "secret"), ("token_location", "header")),
    (
      ("cookie_samesite", "lax"),
      ("secret_key", "secret"),
      ("token_location", "header"),
    ),
    (
      ("cookie_samesite", "strict"),
      ("secret_key", "secret"),
      ("token_location", "header"),
    ),
  ),
  ids=("cookie-headers", "cookie-headers-samesite-lax", "cookie-headers-samesite-strict"),
)
def test_submit_csrf_token_in_headers_and_cookie(
  csrf_settings: Tuple[Tuple[str, str], ...], test_client: TestClient
):
  ### Load config ###
  @CsrfProtect.load_config
  def get_configs():
    return csrf_settings

  ### Generate token ###
  response = test_client.get("/gen-token")
  assert response.status_code == 200

  ### Asserts that `cookie_token` is present
  cookie_token: Optional[str] = test_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is not None

  ### Extract `csrf_token` from response to be set as next request's header ###
  csrf_token: Optional[str] = response.json().get("csrf_token", None)
  assert csrf_token is not None
  headers: Dict[str, str] = {"X-CSRF-Token": csrf_token}

  ### Post to protected endpoint ###
  response = test_client.post("/protected", headers=headers)

  ### Assertions ###
  csrf_token = response.json().get("fastapi-csrf-token")
  assert csrf_token is None
  assert response.status_code == 200
  assert response.json() == {"detail": "OK"}
  cookie_token = test_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is None

  ### Immediately get protected contents again ###
  response = test_client.post("/protected", headers=headers)

  ### Assertions ###
  assert response.status_code == 400
  assert response.json() == {"detail": "Missing Cookie: `fastapi-csrf-token`."}


@mark.parametrize(
  "csrf_settings",
  (
    (("cookie_secure", True), ("secret_key", "secret"), ("token_location", "header")),
    (
      ("cookie_samesite", "lax"),
      ("cookie_secure", True),
      ("secret_key", "secret"),
      ("token_location", "header"),
    ),
    (
      ("cookie_samesite", "none"),
      ("cookie_secure", True),
      ("secret_key", "secret"),
      ("token_location", "header"),
    ),
    (
      ("cookie_samesite", "strict"),
      ("cookie_secure", True),
      ("secret_key", "secret"),
      ("token_location", "header"),
    ),
  ),
  ids=(
    "cookie-headers-secure",
    "cookie-headers-samesite-lax-secure",
    "cookie-headers-samesite-none-secure",
    "cookie-headers-samesite-strict-secure",
  ),
)
def test_submit_csrf_token_in_headers_and_cookie_secure(
  csrf_settings: Tuple[Tuple[str, str], ...], test_client: TestClient
):
  ### Bypass TestClient base_url to https for `Secure` cookies ###
  test_client.base_url = "https://testserver"

  ### Load config ###
  @CsrfProtect.load_config
  def get_configs():
    return csrf_settings

  ### Generate token ###
  response = test_client.get("/gen-token")
  assert response.status_code == 200

  ### Asserts that `cookie_token` is present
  cookie_token: Optional[str] = test_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is not None

  ### Extract `csrf_token` from response to be set as next request's header ###
  csrf_token: Optional[str] = response.json().get("csrf_token", None)
  assert csrf_token is not None
  headers: Dict[str, str] = {"X-CSRF-Token": csrf_token}

  ### Post to protected endpoint ###
  response = test_client.post("/protected", headers=headers)

  ### Assertions ###
  csrf_token = response.json().get("fastapi-csrf-token")
  assert csrf_token is None
  assert response.status_code == 200
  assert response.json() == {"detail": "OK"}
  cookie_token = test_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is None

  ### Immediately get protected contents again ###
  response = test_client.post("/protected", headers=headers)

  ### Assertions ###
  assert response.status_code == 400
  assert response.json() == {"detail": "Missing Cookie: `fastapi-csrf-token`."}
