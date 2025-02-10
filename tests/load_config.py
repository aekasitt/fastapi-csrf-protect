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
  "csrf_settings, reason",
  (
    ((("cookie_samesite", None),), "value_error"),
    ((("cookie_samesite", "none"),), "value_error"),
    ((("cookie_samesite", b"lax"),), "literal_error"),
    ((("cookie_samesite", b"none"),), "literal_error"),
    ((("cookie_samesite", b"strict"),), "literal_error"),
    ((("cookie_samesite", "null"),), "literal_error"),
    ((("cookie_samesite", b"null"),), "literal_error"),
    ((("cookie_samesite", 0),), "literal_error"),
    ((("cookie_samesite", 1),), "literal_error"),
    ((("cookie_samesite", True),), "literal_error"),
    ((("cookie_samesite", False),), "literal_error"),
    ((("cookie_samesite", 2.0),), "literal_error"),
    ((("cookie_samesite", {1, 2, 3}),), "literal_error"),
    ((("cookie_samesite", {1.0, 2.0, 3.0}),), "literal_error"),
    ((("cookie_samesite", {"1", "2", "3"}),), "literal_error"),
    ((("cookie_samesite", [1, 2, 3]),), "literal_error"),
    ((("cookie_samesite", [1.0, 2.0, 3.0]),), "literal_error"),
    ((("cookie_samesite", ["1", "2", "3"]),), "literal_error"),
    ((("cookie_samesite", {"key": "value"}),), "literal_error"),
    ((("cookie_secure", "false"),), "bool_type"),
    ((("cookie_secure", b"true"),), "bool_type"),
    ((("header_name", 2),), "string_type"),
    ((("header_name", 1.0),), "string_type"),
    ((("header_name", True),), "string_type"),
    ((("header_name", b"header_name"),), "string_type"),
    ((("header_name", []),), "string_type"),
    ((("header_name", {}),), "string_type"),
    ((("header_type", 2),), "string_type"),
    ((("header_type", 1.0),), "string_type"),
    ((("header_type", True),), "string_type"),
    ((("header_type", b"header_type"),), "string_type"),
    ((("header_type", []),), "string_type"),
    ((("header_type", {}),), "string_type"),
    ((("httponly", "false"),), "bool_type"),
    ((("httponly", b"true"),), "bool_type"),
    ((("methods", 2),), "set_type"),
    ((("methods", 1.0),), "set_type"),
    ((("methods", True),), "set_type"),
    ((("methods", b"GET, POST"),), "set_type"),
    ((("methods", "GET, POST"),), "set_type"),
    ((("methods", {}),), "set_type"),
    ((("methods", [1, 2, 3]),), "literal_error"),
    ((("methods", (1, 2, 3)),), "literal_error"),
    ((("methods", {1, 2, 3}),), "literal_error"),
    ((("methods", ["1", "2", "3"]),), "literal_error"),
    ((("methods", ("1", "2", "3")),), "literal_error"),
    ((("methods", {"1", "2", "3"}),), "literal_error"),
    ((("methods", {"key": "value"}),), "set_type"),
    ((("secret_key", 2),), "string_type"),
    ((("secret_key", 1.0),), "string_type"),
    ((("secret_key", True),), "string_type"),
    ((("secret_key", b"secret"),), "string_type"),
    ((("secret_key", []),), "string_type"),
    ((("secret_key", {}),), "string_type"),
    ((("token_location", "body"),), "value_error"),
    ((("token_location", b"body"), ("token_key", "csrf-token")), "literal_error"),
    ((("token_location", b"header"),), "literal_error"),
  ),
  ids=[
    "cookie-samesite-None",
    "cookie-samesite-none",
    "cookie-samesite-none-as-bytes",
    "cookie-samesite-lax-as-bytes",
    "cookie-samesite-strict-as-bytes",
    "cookie-samesite-null",
    "cookie-samesite-null-as-bytes",
    "cookie-samesite-0",
    "cookie-samesite-1",
    "cookie-samesite-True",
    "cookie-samesite-False",
    "cookie-samesite-2.0",
    "cookie-samesite-set-1-2-3",
    "cookie-samesite-set-1.0-2.0-3.0",
    "cookie-samesite-set-1-2-3-as-strings",
    "cookie-samesite-list-1-2-3",
    "cookie-samesite-list-1.0-2.0-3.0",
    "cookie-samesite-list-1-2-3-as-strings",
    "cookie-samesite-dict-key-value",
    "cookie-secure-false",
    "cookie-secure-true-as-bytes",
    "header-name-2",
    "header-name-1.0",
    "header-name-True",
    "header-name-header-name-as-bytes",
    "header-name-empty-list",
    "header-name-empty-set",
    "header-type-2",
    "header-type-1.0",
    "header-type-True",
    "header-type-header-type-as-bytes",
    "header-type-empty-list",
    "header-type-empty-set",
    "httponly-false",
    "httponly-true-as-bytes",
    "methods-2",
    "methods-1.0",
    "methods-True",
    "methods-GET,POST-as-bytes",
    "methods-GET,POST",
    "methods-empty-dict",
    "methods-empty-list-1-2-3",
    "methods-empty-tuple-1-2-3",
    "methods-empty-list-1-2-3-as-strings",
    "methods-empty-tuple-1-2-3-as-strings",
    "methods-empty-set-1-2-3-as-strings",
    "methods-empty-dict-key-value",
    "secret-key-2",
    "secret-key-1.0",
    "secret-key-True",
    "secret-key-secret-as-bytes",
    "secret-key-empty-list",
    "secret-key-empty-set",
    "token-location-body-without-token-key",
    "token-location-body-as-bytes-with-token-key",
    "token-location-body-as-bytes-with-token-key",
    "token-location-header-as-bytes",
  ],
)
def test_load_config_with_invalid_csrf_settings(
  csrf_settings: Tuple[Tuple[str, Union[None, bool, bytes, float, int, str]], ...], reason: str
) -> None:
  with raises(ValidationError) as exc_info:

    @CsrfProtect.load_config
    def _() -> Tuple[Tuple[str, Union[None, bool, bytes, int, float, str]], ...]:
      return csrf_settings

  assert exc_info is not None
  assert f"[type={reason}" in str(exc_info.value)


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
