#!/usr/bin/env python3
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/tests/token_invalid.py
# VERSION:     1.0.2
# CREATED:     2020-11-26 16:14
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Dict, List, Tuple

### Third-party packages ###
from fastapi.testclient import TestClient
from warnings import filterwarnings

### Local modules ###
from . import test_client
from fastapi_csrf_protect import CsrfProtect


def test_validate_token_invalid_request(test_client: TestClient) -> None:
  @CsrfProtect.load_config
  def _() -> List[Tuple[str, str]]:
    return [("secret_key", "secret"), ("cookie_key", "fastapi-csrf-token")]

  ### Ignore DeprecationWarnings when setting cookie manually with FastAPI TestClient ###
  filterwarnings("ignore", category=DeprecationWarning)

  ### Post to protected endpoint ###
  headers: Dict[str, str] = {"X-CSRF-Token": "invalid"}
  response = test_client.post(
    "/protected", cookies={"fastapi-csrf-token": "invalid"}, headers=headers
  )

  ### Assertions ###
  assert response.status_code == 401
  assert response.json() == {"detail": "The CSRF token is invalid."}
