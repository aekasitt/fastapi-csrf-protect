#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/tests/flexible/token_invalid.py
# VERSION:     1.0.7
# CREATED:     2025-08-18 08:53:00+02:00
# AUTHOR:      Eliam Lotonga <e.m.lotonga@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from fastapi.testclient import TestClient
from warnings import filterwarnings

### Local modules ###
from fastapi_csrf_protect.flexible import CsrfProtect
from tests.flexible import flexible_client


def test_validate_token_invalid_request(flexible_client: TestClient) -> None:
  @CsrfProtect.load_config
  def _() -> tuple[tuple[str, str], ...]:
    return (("secret_key", "secret"), ("cookie_key", "fastapi-csrf-token"))

  ### Ignore DeprecationWarnings when setting cookie manually with FastAPI TestClient ###
  filterwarnings("ignore", category=DeprecationWarning)

  ### Post to protected endpoint ###
  headers: dict[str, str] = {"X-CSRF-Token": "invalid"}
  response = flexible_client.post(
    "/protected", cookies={"fastapi-csrf-token": "invalid"}, headers=headers
  )

  ### Assertions ###
  assert response.status_code == 401
  assert response.json() == {"detail": "The CSRF token is invalid."}
