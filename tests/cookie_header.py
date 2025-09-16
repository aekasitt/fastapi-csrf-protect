#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/tests/cookie_header.py
# VERSION:     1.0.7
# CREATED:     2025-02-04 11:14
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Optional

### Third-party packages ###
from fastapi.testclient import TestClient
from httpx import Response, URL
from pytest import mark

### Local modules ###
from fastapi_csrf_protect import CsrfProtect
from tests import test_client


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
  csrf_settings: tuple[tuple[str, str], ...], test_client: TestClient
) -> None:
  ### Load config ###
  @CsrfProtect.load_config
  def _() -> tuple[tuple[str, str], ...]:
    return csrf_settings

  ### Generate token ###
  response: Response = test_client.get("/gen-token")
  assert response.status_code == 200

  ### Asserts that `cookie_token` is present
  cookie_token: Optional[str] = test_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is not None

  ### Extract `csrf_token` from response to be set as next request's header ###
  csrf_token: Optional[str] = response.json().get("csrf_token", None)
  assert csrf_token is not None
  headers: dict[str, str] = {"X-CSRF-Token": csrf_token}

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
    (
      ("cookie_secure", True),
      ("secret_key", "secret"),
      ("token_location", "header"),
    ),
  ),
  ids=("cookie-header-secure-http",),
)
def test_submit_csrf_token_in_headers_and_cookies_secure_but_using_http(
  csrf_settings: tuple[tuple[str, str], ...], test_client: TestClient
) -> None:
  ### Load config ###
  @CsrfProtect.load_config
  def _() -> tuple[tuple[str, str], ...]:
    return csrf_settings

  ### Generate token ###
  response: Response = test_client.get("/gen-token")
  assert response.status_code == 200

  ### Asserts that `cookie_token` is present
  cookie_token: Optional[str] = test_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is not None

  ### Extract `csrf_token` from response to be set as next request's body ###
  csrf_token: Optional[str] = response.json().get("csrf_token", None)
  headers: dict[str, str] = {"X-CSRF-Token": csrf_token} if csrf_token is not None else {}

  ### Post to protected endpoint but fails because TestClients defaults to http ###
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
    "cookie-header-secure-https",
    "cookie-header-samesite-lax-secure-https",
    "cookie-header-samesite-none-secure-https",
    "cookie-header-samesite-strict-secure-https",
  ),
)
def test_submit_csrf_token_in_headers_and_cookie_secure(
  csrf_settings: tuple[tuple[str, str], ...], test_client: TestClient
) -> None:
  ### Bypass TestClient base_url to https for `Secure` cookies ###
  test_client.base_url = URL("https://testserver")

  ### Load config ###
  @CsrfProtect.load_config
  def _() -> tuple[tuple[str, str], ...]:
    return csrf_settings

  ### Generate token ###
  response: Response = test_client.get("/gen-token")
  assert response.status_code == 200

  ### Asserts that `cookie_token` is present
  cookie_token: Optional[str] = test_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is not None

  ### Extract `csrf_token` from response to be set as next request's header ###
  csrf_token: Optional[str] = response.json().get("csrf_token", None)
  assert csrf_token is not None
  headers: dict[str, str] = {"X-CSRF-Token": csrf_token}

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
