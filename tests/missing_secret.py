#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/tests/missing_secret.py
# VERSION:     1.0.7
# CREATED:     2021-08-18 23:58
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from fastapi.testclient import TestClient
from pytest import raises

### Local modules ###
from fastapi_csrf_protect import CsrfProtect
from tests import test_client


def test_validate_missing_secret_key(test_client: TestClient) -> None:
  with raises(RuntimeError) as err:

    @CsrfProtect.load_config
    def _() -> tuple[tuple[str, None], ...]:
      return (("secret_key", None),)

    test_client.get("/gen-token")
  assert err.match("A secret key is required to use CsrfProtect extension.")
