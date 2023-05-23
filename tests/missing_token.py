#!/usr/bin/env python3
# Copyright (C) 2021-2023 All rights reserved.
# FILENAME:  missing_token.py
# VERSION: 	 0.3.0
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
    ### Loads config ###
    @CsrfProtect.load_config
    def get_secret_key():
        return [("secret_key", "secret")]

    ### Generate token ###
    response = test_client.get("/gen-token")
    csrf_token: str = response.json().get("csrf_token", None)
    headers: dict = {"X-CSRF-Token": csrf_token} if csrf_token is not None else {}

    ### Clear previously received cookies ###
    test_client.cookies = None  # type: ignore

    ### Get protected contents ###
    response = test_client.get("/protected", headers=headers)

    ### Assertions ###
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing Cookie: `fastapi-csrf-token`."}


def test_validate_missing_header_token_request(test_client: TestClient):
    ### Loads Config ###
    @CsrfProtect.load_config
    def get_secret_key():
        return [("secret_key", "secret")]

    ### Get CSRF Tokens ###
    response = test_client.get("/gen-token")

    ### Get protected contents ###
    response = test_client.get("/protected")

    ### Assertions ###
    assert response.status_code == 422
    assert response.json() == {
        "detail": 'Bad headers. Expected "X-CSRF-Token" in headers'
    }
