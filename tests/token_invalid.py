#!/usr/bin/env python3
# Copyright (C) 2021-2023 All rights reserved.
# FILENAME:  token_invalid.py
# VERSION: 	 0.2.2
# CREATED: 	 2020-11-26 16:14
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
### Third-Party Packages ###
from fastapi.testclient import TestClient
from warnings import filterwarnings

### Local Modules ###
from . import test_client
from fastapi_csrf_protect import CsrfProtect


def test_validate_token_invalid_request(test_client: TestClient):
    @CsrfProtect.load_config
    def get_configs():
        return [("secret_key", "secret"), ("cookie-key", "fastapi-csrf-token")]

    ### Ignore DeprecationWarnings when setting cookie manually with FastAPI TestClient ###
    filterwarnings("ignore", category=DeprecationWarning)

    ### Get ###
    headers: dict = {"X-CSRF-Token": "invalid"}
    response = test_client.get(
        "/protected", cookies={"fastapi-csrf-token": "invalid"}, headers=headers
    )

    ### Assertions ###
    assert response.status_code == 401
    assert response.json() == {"detail": "The CSRF token is invalid."}
