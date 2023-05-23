#!/usr/bin/env python3
# Copyright (C) 2021-2023 All rights reserved.
# FILENAME:  token_expired.py
# VERSION: 	 0.2.2
# CREATED: 	 2020-11-26 16:14
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
### Standard Packages ###
from time import sleep
from warnings import filterwarnings

### Third-Party Packages ###
from . import test_client
from fastapi.testclient import TestClient

### Local Modules ###
from . import *
from fastapi_csrf_protect import CsrfProtect


def test_validate_token_expired(test_client: TestClient, max_age: int = 2):
    ### Loads Config ###
    @CsrfProtect.load_config
    def get_configs():
        return [("secret_key", "secret"), ("max_age", max_age)]

    ### Get ###
    response = test_client.get("/set-csrf-tokens")

    ### Assertion ###
    assert response.status_code == 200
    csrf_token: str = response.json().get("csrf_token", None)
    headers: dict = {"X-CSRF-Token": csrf_token} if csrf_token is not None else {}

    ### Ignore DeprecationWarnings when setting cookie manually with FastAPI TestClient ###
    filterwarnings("ignore", category=DeprecationWarning)

    ### Get Protected Contents ###
    response = test_client.get("/protected", cookies=response.cookies, headers=headers)

    ### Assertions ###
    assert response.status_code == 200
    assert response.json() == {"detail": "OK"}

    ### Delays ###
    sleep(max_age + 1)

    ### Get Protected Contents ###
    response = test_client.get("/protected", cookies=response.cookies, headers=headers)

    ### Assertions ###
    assert response.status_code == 401
    assert response.json() == {"detail": "The CSRF token has expired."}
