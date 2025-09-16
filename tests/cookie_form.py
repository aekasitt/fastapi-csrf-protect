#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/tests/cookie_form.py
# VERSION:     1.0.7
# CREATED:     2025-09-11 16:09
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Optional
from urllib.parse import urlencode

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
    (("secret_key", "secret"), ("token_key", "csrf-token"), ("token_location", "body")),
    (
      ("cookie_samesite", "lax"),
      ("secret_key", "secret"),
      ("token_key", "csrf-token"),
      ("token_location", "body"),
    ),
    (
      ("cookie_samesite", "strict"),
      ("secret_key", "secret"),
      ("token_key", "csrf-token"),
      ("token_location", "body"),
    ),
  ),
  ids=("cookie-form", "cookie-form-samesite-lax", "cookie-form-samesite-strict"),
)
def test_submit_csrf_token_in_form_and_cookie(
  csrf_settings: tuple[tuple[str, str], ...], test_client: TestClient
) -> None:
  ### Load config ###
  @CsrfProtect.load_config
  def _() -> tuple[tuple[str, str], ...]:
    return csrf_settings

  ### Form headers ###
  headers: dict[str, str] = {"Content-Type": "application/x-www-form-urlencoded"}

  ### Generate token ###
  response: Response = test_client.get("/gen-token")
  assert response.status_code == 200

  ### Asserts that `cookie_token` is present
  cookie_token: Optional[str] = test_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is not None

  ### Extract `csrf_token` from response to be set as next request's body ###
  csrf_token: Optional[str] = response.json().get("csrf_token", None)
  payload: dict[str, str] = {"csrf-token": csrf_token} if csrf_token is not None else {}
  content: bytes = urlencode(payload).encode("utf-8")

  ### Post to protected endpoint ###
  response = test_client.post("/protected", content=content, headers=headers)

  ### Assertions ###
  assert response.status_code == 200
  assert response.json() == {"detail": "OK"}
  cookie_token = test_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is None

  ### Immediately get protected contents again ###
  response = test_client.post("/protected", content=content, headers=headers)

  ### Assertions ###
  assert response.status_code == 400
  assert response.json() == {"detail": "Missing Cookie: `fastapi-csrf-token`."}


@mark.parametrize(
  "csrf_settings",
  (
    (
      ("cookie_secure", True),
      ("secret_key", "secret"),
      ("token_key", "csrf-token"),
      ("token_location", "body"),
    ),
  ),
  ids=("cookie-form-secure-http",),
)
def test_submit_csrf_token_in_form_and_cookies_secure_but_using_http(
  csrf_settings: tuple[tuple[str, str], ...], test_client: TestClient
) -> None:
  ### Load config ###
  @CsrfProtect.load_config
  def _() -> tuple[tuple[str, str], ...]:
    return csrf_settings

  ### Form headers ###
  headers: dict[str, str] = {"Content-Type": "application/x-www-form-urlencoded"}

  ### Generate token ###
  response: Response = test_client.get("/gen-token")
  assert response.status_code == 200

  ### Asserts that `cookie_token` is present
  cookie_token: Optional[str] = test_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is not None

  ### Extract `csrf_token` from response to be set as next request's form ###
  csrf_token: Optional[str] = response.json().get("csrf_token", None)
  payload: dict[str, str] = {"csrf-token": csrf_token} if csrf_token is not None else {}
  content: bytes = urlencode(payload).encode("utf-8")

  ### Post to protected endpoint but fails because TestClients defaults to http ###
  response = test_client.post("/protected", content=content, headers=headers)

  ### Assertions ###
  assert response.status_code == 400
  assert response.json() == {"detail": "Missing Cookie: `fastapi-csrf-token`."}


@mark.parametrize(
  "csrf_settings",
  (
    (
      ("cookie_secure", True),
      ("secret_key", "secret"),
      ("token_key", "csrf-token"),
      ("token_location", "body"),
    ),
    (
      ("cookie_samesite", "lax"),
      ("cookie_secure", True),
      ("secret_key", "secret"),
      ("token_key", "csrf-token"),
      ("token_location", "body"),
    ),
    (
      ("cookie_samesite", "none"),
      ("cookie_secure", True),
      ("secret_key", "secret"),
      ("token_key", "csrf-token"),
      ("token_location", "body"),
    ),
    (
      ("cookie_samesite", "strict"),
      ("cookie_secure", True),
      ("secret_key", "secret"),
      ("token_key", "csrf-token"),
      ("token_location", "body"),
    ),
  ),
  ids=(
    "cookie-form-secure-https",
    "cookie-form-samesite-lax-secure-https",
    "cookie-form-samesite-none-secure-https",
    "cookie-form-samesite-strict-secure-https",
  ),
)
def test_submit_csrf_token_in_form_and_cookies_secure(
  csrf_settings: tuple[tuple[str, str], ...], test_client: TestClient
) -> None:
  ### Bypass TestClient base_url to https for `Secure` cookies ###
  test_client.base_url = URL("https://testserver")

  ### Form headers ###
  headers: dict[str, str] = {"Content-Type": "application/x-www-form-urlencoded"}

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

  ### Extract `csrf_token` from response to be set as next request's form ###
  csrf_token: Optional[str] = response.json().get("csrf_token", None)
  payload: dict[str, str] = {"csrf-token": csrf_token} if csrf_token is not None else {}
  content: bytes = urlencode(payload).encode("utf-8")

  ### Post to protected endpoint ###
  response = test_client.post("/protected", content=content, headers=headers)

  ### Assertions ###
  assert response.status_code == 200
  assert response.json() == {"detail": "OK"}
  cookie_token = test_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is None

  ### Immediately get protected contents again ###
  response = test_client.post("/protected", content=content, headers=headers)

  ### Assertions ###
  assert response.status_code == 400
  assert response.json() == {"detail": "Missing Cookie: `fastapi-csrf-token`."}
