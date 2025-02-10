#!/usr/bin/env python3
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/tests/load_config.py
# VERSION:     1.0.1
# CREATED:     2020-11-26 16:14
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Tuple, Union

### Third-party packages ###
from pydantic import ValidationError
from pytest import mark, raises

### Local modules ###
from fastapi_csrf_protect import CsrfProtect


@mark.parametrize(
  "csrf_settings",
  (
    (("cookie_samesite", None),),
    (("cookie_samesite", "none"),),
    (("cookie_samesite", b"lax"),),
    (("cookie_samesite", b"none"),),
    (("cookie_samesite", b"strict"),),
    (("cookie_samesite", "null"),),
    (("cookie_samesite", b"null"),),
    (("cookie_samesite", 0),),
    (("cookie_samesite", 1),),
    (("cookie_samesite", True),),
    (("cookie_samesite", False),),
    (("cookie_samesite", 2.0),),
    (("cookie_samesite", {1, 2, 3}),),
    (("cookie_samesite", {1.0, 2.0, 3.0}),),
    (("cookie_samesite", {"1", "2", "3"}),),
    (("cookie_samesite", [1, 2, 3]),),
    (("cookie_samesite", [1.0, 2.0, 3.0]),),
    (("cookie_samesite", ["1", "2", "3"]),),
    (("cookie_samesite", {"key": "value"}),),
    (("cookie_secure", "false"),),
    (("cookie_secure", b"true"),),
    (("header_name", 2),),
    (("header_name", 1.0),),
    (("header_name", True),),
    (("header_name", b"header_name"),),
    (("header_name", []),),
    (("header_name", {}),),
    (("header_type", 2),),
    (("header_type", 1.0),),
    (("header_type", True),),
    (("header_type", b"header_type"),),
    (("header_type", []),),
    (("header_type", {}),),
    (("httponly", "false"),),
    (("httponly", b"true"),),
    (("methods", 2),),
    (("methods", 1.0),),
    (("methods", True),),
    (("methods", b"GET, POST"),),
    (("methods", "GET, POST"),),
    (("methods", {}),),
    (("methods", [1, 2, 3]),),
    (("methods", (1, 2, 3)),),
    (("methods", {1, 2, 3}),),
    (("methods", ["1", "2", "3"]),),
    (("methods", ("1", "2", "3")),),
    (("methods", {"1", "2", "3"}),),
    (("methods", {"key": "value"}),),
    (("secret_key", 2),),
    (("secret_key", 1.0),),
    (("secret_key", True),),
    (("secret_key", b"secret"),),
    (("secret_key", []),),
    (("secret_key", {}),),
    (("token_location", "body"),),  # missing token_key
    (("token_location", b"body"), ("token_key", "csrf-token")),
    (("token_location", b"header"),),
  ),
)
def test_load_config_with_invalid_csrf_settings(
  csrf_settings: Tuple[Tuple[str, Union[None, bool, bytes, float, int, str]], ...],
) -> None:
  with raises(ValidationError) as exc_info:

    @CsrfProtect.load_config
    def _() -> Tuple[Tuple[str, Union[None, bool, bytes, int, float, str]], ...]:
      return csrf_settings

  assert exc_info is not None


@mark.parametrize(
  "csrf_settings",
  (
    (("header_name", "header_name"),),
    (("header_type", "header_type"),),
    (("httponly", False),),
    (("httponly", None),),
    (("httponly", True),),
    (("methods", []),),
    (("methods", ["GET", "POST", "DELETE"]),),
    (("methods", ("GET", "POST", "DELETE")),),
    (("methods", {"GET", "POST", "DELETE"}),),
    (("secret_key", "secret"),),
    (("token_location", "body"), ("token_key", "csrf-token")),
    (("token_location", "header"),),
    (("cookie_samesite", None), ("cookie_secure", True)),
    (("cookie_samesite", "lax"),),
    (("cookie_samesite", "none"), ("cookie_secure", True)),
    (("cookie_samesite", "strict"),),
    (("cookie_secure", False),),
    (("cookie_secure", None),),
    (("cookie_secure", True),),
  ),
)
def test_valid_load_config(
  csrf_settings: Tuple[Tuple[str, Union[None, bool, bytes, int, float, str]], ...],
):
  @CsrfProtect.load_config
  def _() -> Tuple[Tuple[str, Union[None, bool, bytes, int, float, str]], ...]:
    return csrf_settings
