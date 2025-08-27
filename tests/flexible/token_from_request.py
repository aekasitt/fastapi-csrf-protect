#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/tests/flexible/token_from_request.py
# VERSION:     1.0.6
# CREATED:     2025-08-22 11:35:00+02:00
# AUTHOR:      Eliam Lotonga <e.m.lotonga@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
from typing import Optional

### Third-party packages ###
from fastapi.testclient import TestClient
from warnings import filterwarnings
from httpx import Response
from pytest import mark

### Local modules ###
from fastapi_csrf_protect.flexible import CsrfProtect
from tests.flexible import flexible_client


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
def test_get_csrf_token_from_request_with_json(csrf_settings, flexible_client):
  ### Load config ###
  @CsrfProtect.load_config
  def _() -> tuple[tuple[str, str], ...]:
    return csrf_settings

  ### Generate token ###
  response: Response = flexible_client.get("/gen-token")
  assert response.status_code == 200

  ### Extract `csrf_token` from response to be set as next request's body ###
  csrf_token: Optional[str] = response.json().get("csrf_token", None)
  assert csrf_token is not None

  ### Post to protected endpoint ###
  response = flexible_client.post("/protected", json={"csrf-token": csrf_token})

  ### Assertions ###
  assert response.status_code == 200
  assert response.json() == {"detail": "OK"}


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
def test_get_csrf_token_from_request_with_form(csrf_settings, flexible_client):
  ### Load config ###
  @CsrfProtect.load_config
  def _() -> tuple[tuple[str, str], ...]:
    return csrf_settings

  ### Generate token ###
  response: Response = flexible_client.get("/gen-token")
  assert response.status_code == 200

  ### Extract `csrf_token` from response to be set as next request's body ###
  csrf_token: Optional[str] = response.json().get("csrf_token", None)
  assert csrf_token is not None

  ### Post to protected endpoint ###
  response = flexible_client.post("/protected", data={"csrf-token": csrf_token})

  ### Assertions ###
  assert response.status_code == 200
  assert response.json() == {"detail": "OK"}


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
def test_get_csrf_token_from_request_without_token(csrf_settings, flexible_client):
  ### Load config ###
  @CsrfProtect.load_config
  def foo() -> tuple[tuple[str, str], ...]:
    return csrf_settings

  ### Post to protected endpoint ###
  response = flexible_client.post("/protected")

  ### Assertions ###
  assert response.status_code == 400
  assert response.json() == {'detail': 'Missing Cookie: `fastapi-csrf-token`.'}
