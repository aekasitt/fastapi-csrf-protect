#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/tests/flexible/cookie.py
# VERSION:     1.0.5
# CREATED:     2025-08-11 16:02:06+02:00
# AUTHOR:      Eliam Lotonga <e.m.lotonga@gmail.com>
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
from fastapi_csrf_protect.flexible import CsrfProtect
from tests.flexible import flexible_client


@mark.parametrize(
  "csrf_settings",
  (
    (("cookie_secure", True), ("secret_key", "secret")),
    (
      ("cookie_samesite", "lax"),
      ("cookie_secure", True),
      ("secret_key", "secret"),
    ),
    (
      ("cookie_samesite", "none"),
      ("cookie_secure", True),
      ("secret_key", "secret"),
    ),
    (
      ("cookie_samesite", "strict"),
      ("cookie_secure", True),
      ("secret_key", "secret"),
    ),
  ),
  ids=(
    "cookie-headers-secure",
    "cookie-headers-samesite-lax-secure",
    "cookie-headers-samesite-none-secure",
    "cookie-headers-samesite-strict-secure",
  ),
)
def test_submit_csrf_token_in_headers_or_body_and_cookie_secure(
  csrf_settings: tuple[tuple[str, str], ...], flexible_client: TestClient
) -> None:
  ### Bypass TestClient base_url to https for `Secure` cookies ###
  flexible_client.base_url = URL("https://testserver")

  ### Load config ###
  @CsrfProtect.load_config
  def _() -> tuple[tuple[str, str], ...]:
    return csrf_settings

  ### Generate token ###
  response: Response = flexible_client.get("/gen-token")
  assert response.status_code == 200

  ### Asserts that `cookie_token` is present
  cookie_token: Optional[str] = flexible_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is not None

  ### Extract `csrf_token` from response to be set as next request's header ###
  csrf_token: Optional[str] = response.json().get("csrf_token", None)
  assert csrf_token is not None
  headers: dict[str, str] = {"X-CSRF-Token": csrf_token}

  ### Post to protected endpoint ###
  response = flexible_client.post("/protected", headers=headers)

  ### Assertions ###
  csrf_token = response.json().get("fastapi-csrf-token")
  assert csrf_token is None
  assert response.status_code == 200
  assert response.json() == {"detail": "OK"}
  cookie_token = flexible_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is None

  ### Immediately get protected contents again ###
  response = flexible_client.post("/protected", headers=headers)

  ### Assertions ###
  assert response.status_code == 400
  assert response.json() == {"detail": "Missing Cookie: `fastapi-csrf-token`."}


@mark.parametrize(
  "csrf_settings",
  (
    (("secret_key", "secret"), ("token_key", "csrf-token")),
    (
      ("cookie_samesite", "lax"),
      ("secret_key", "secret"),
      ("token_key", "csrf-token"),
    ),
    (
      ("cookie_samesite", "strict"),
      ("secret_key", "secret"),
      ("token_key", "csrf-token"),
    ),
  ),
  ids=("cookie-body", "cookie-body-samesite-lax", "cookie-body-samesite-strict"),
)
def test_submit_csrf_token_in_body_and_cookies(
  csrf_settings: tuple[tuple[str, str], ...], flexible_client: TestClient
) -> None:
  ### Load config ###
  @CsrfProtect.load_config
  def _() -> tuple[tuple[str, str], ...]:
    return csrf_settings

  ### Generate token ###
  response: Response = flexible_client.get("/gen-token")
  assert response.status_code == 200

  ### Asserts that `cookie_token` is present
  cookie_token: Optional[str] = flexible_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is not None

  ### Extract `csrf_token` from response to be set as next request's body ###
  csrf_token: Optional[str] = response.json().get("csrf_token", None)
  payload: dict[str, str] = {"csrf-token": csrf_token} if csrf_token is not None else {}

  ### Post to protected endpoint ###
  response = flexible_client.post("/protected", data=payload)
  print(response.text)

  ### Assertions ###
  assert response.status_code == 200
  assert response.json() == {"detail": "OK"}
  cookie_token = flexible_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is None

  ### Immediately get protected contents again ###
  response = flexible_client.post("/protected", data=payload)

  ### Assertions ###
  assert response.status_code == 400
  assert response.json() == {"detail": "Missing Cookie: `fastapi-csrf-token`."}
