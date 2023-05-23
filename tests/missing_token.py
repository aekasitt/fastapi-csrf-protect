#!/usr/bin/env python3
# Copyright (C) 2021-2023 All rights reserved.
# FILENAME:  missing_token.py
# VERSION: 	 0.2.2
# CREATED: 	 2020-11-26 16:14
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
### Third-Party Packages ###
from fastapi.testclient import TestClient

### Local Packages ###
from . import test_client
from fastapi_csrf_protect import CsrfProtect


def test_validate_missing_cookie_token_request(test_client: TestClient):
    ### Loads Config ###
    @CsrfProtect.load_config
    def get_secret_key():
        return [("secret_key", "secret")]
    
    ### Get CSRF Tokens ###
    response = test_client.get("/set-csrf-tokens")
    csrf_token: str = response.json().get("csrf_token", None)
    headers: dict = {"X-CSRF-Token": csrf_token} if csrf_token is not None else {}

    ### Get Protected Contents ###
    response = test_client.get("/protected", headers=headers)

    ### Assertions ###
    assert response.status_code == 401
    assert response.json() == {"detail": "The CSRF token pair submitted do not match."}


def test_validate_missing_header_token_request(test_client: TestClient):
    ### Loads Config ###
    @CsrfProtect.load_config
    def get_secret_key():
        return [("secret_key", "secret")]

    ### Get CSRF Tokens ###
    response = test_client.get("/set-csrf-tokens")

    ### Get Protected Contents ###
    response = test_client.get("/protected", cookies=response.cookies)

    ### Assertions ###
    assert response.status_code == 422
    assert response.json() == {"detail": 'Bad headers. Expected "X-CSRF-Token" in headers'}
