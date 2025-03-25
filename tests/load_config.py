#!/usr/bin/env python3
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/tests/load_config.py
# VERSION:     1.0.2
# CREATED:     2020-11-26 16:14
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Tuple, Union

### Third-party packages ###
from pytest import mark, raises

### Local modules ###
from fastapi_csrf_protect import CsrfProtect


@mark.parametrize(
  "csrf_settings, reason",
  (
    ((("cookie_samesite", None),), "CsrfConfig must be a sequence of tuples"),
    ((("cookie_samesite", "none"),), "CsrfConfig must be a sequence of tuples"),
    ((("cookie_samesite", b"lax"),), "CsrfConfig must be a sequence of tuples"),
    ((("cookie_samesite", b"none"),), "CsrfConfig must be a sequence of tuples"),
    ((("cookie_samesite", b"strict"),), "CsrfConfig must be a sequence of tuples"),
    ((("cookie_samesite", "null"),), "CsrfConfig must be a sequence of tuples"),
    ((("cookie_samesite", b"null"),), "CsrfConfig must be a sequence of tuples"),
    ((("cookie_samesite", 0),), "CsrfConfig must be a sequence of tuples"),
    ((("cookie_samesite", 1),), "CsrfConfig must be a sequence of tuples"),
    ((("cookie_samesite", True),), "CsrfConfig must be a sequence of tuples"),
    ((("cookie_samesite", False),), "CsrfConfig must be a sequence of tuples"),
    ((("cookie_samesite", 2.0),), "CsrfConfig must be a sequence of tuples"),
    ((("cookie_samesite", {1, 2, 3}),), "CsrfConfig must be a sequence of tuples"),
    ((("cookie_samesite", {1.0, 2.0, 3.0}),), "CsrfConfig must be a sequence of tuples"),
    ((("cookie_samesite", {"1", "2", "3"}),), "CsrfConfig must be a sequence of tuples"),
    ((("cookie_samesite", [1, 2, 3]),), "CsrfConfig must be a sequence of tuples"),
    ((("cookie_samesite", [1.0, 2.0, 3.0]),), "CsrfConfig must be a sequence of tuples"),
    ((("cookie_samesite", ["1", "2", "3"]),), "CsrfConfig must be a sequence of tuples"),
    ((("cookie_samesite", {"key": "value"}),), "CsrfConfig must be a sequence of tuples"),
    ((("cookie_secure", "false"),), "CsrfConfig must be a sequence of tuples"),
    ((("cookie_secure", b"true"),), "CsrfConfig must be a sequence of tuples"),
    ((("header_name", 2),), "CsrfConfig must be a sequence of tuples"),
    ((("header_name", 1.0),), "CsrfConfig must be a sequence of tuples"),
    ((("header_name", True),), "CsrfConfig must be a sequence of tuples"),
    ((("header_name", b"header_name"),), "CsrfConfig must be a sequence of tuples"),
    ((("header_name", []),), "CsrfConfig must be a sequence of tuples"),
    ((("header_name", {}),), "CsrfConfig must be a sequence of tuples"),
    ((("header_type", 2),), "CsrfConfig must be a sequence of tuples"),
    ((("header_type", 1.0),), "CsrfConfig must be a sequence of tuples"),
    ((("header_type", True),), "CsrfConfig must be a sequence of tuples"),
    ((("header_type", b"header_type"),), "CsrfConfig must be a sequence of tuples"),
    ((("header_type", []),), "CsrfConfig must be a sequence of tuples"),
    ((("header_type", {}),), "CsrfConfig must be a sequence of tuples"),
    ((("httponly", "false"),), "CsrfConfig must be a sequence of tuples"),
    ((("httponly", b"true"),), "CsrfConfig must be a sequence of tuples"),
    ((("methods", 2),), "CsrfConfig must be a sequence of tuples"),
    ((("methods", 1.0),), "CsrfConfig must be a sequence of tuples"),
    ((("methods", True),), "CsrfConfig must be a sequence of tuples"),
    ((("methods", b"GET, POST"),), "CsrfConfig must be a sequence of tuples"),
    ((("methods", "GET, POST"),), "CsrfConfig must be a sequence of tuples"),
    ((("methods", {}),), "CsrfConfig must be a sequence of tuples"),
    ((("methods", [1, 2, 3]),), "CsrfConfig must be a sequence of tuples"),
    ((("methods", (1, 2, 3)),), "CsrfConfig must be a sequence of tuples"),
    ((("methods", {1, 2, 3}),), "CsrfConfig must be a sequence of tuples"),
    ((("methods", ["1", "2", "3"]),), "CsrfConfig must be a sequence of tuples"),
    ((("methods", ("1", "2", "3")),), "CsrfConfig must be a sequence of tuples"),
    ((("methods", {"1", "2", "3"}),), "CsrfConfig must be a sequence of tuples"),
    ((("methods", {"key": "value"}),), "CsrfConfig must be a sequence of tuples"),
    ((("secret_key", 2),), "CsrfConfig must be a sequence of tuples"),
    ((("secret_key", 1.0),), "CsrfConfig must be a sequence of tuples"),
    ((("secret_key", True),), "CsrfConfig must be a sequence of tuples"),
    ((("secret_key", b"secret"),), "CsrfConfig must be a sequence of tuples"),
    ((("secret_key", []),), "CsrfConfig must be a sequence of tuples"),
    ((("secret_key", {}),), "CsrfConfig must be a sequence of tuples"),
    ((("token_location", "body"),), "CsrfConfig must be a sequence of tuples"),
    ((("token_location", b"body"), ("token_key", "csrf-token")), "CsrfConfig must be a sequence of tuples"),
    ((("token_location", b"header"),), "CsrfConfig must be a sequence of tuples"),
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
  with raises(TypeError) as exc_info:

    @CsrfProtect.load_config
    def _() -> Tuple[Tuple[str, Union[None, bool, bytes, int, float, str]], ...]:
      return csrf_settings

  assert exc_info is not None
  assert reason == str(exc_info.value)


@mark.parametrize(
  "csrf_settings",
  (
    (("header_name", "header_name"),),
    (("header_type", "header_type"),),
    (("httponly", False),),
    (("httponly", None),),
    (("httponly", True),),
    # (("methods", []),),  # TODO: uncomment test
    # (("methods", ["GET", "POST", "DELETE"]),),  # TODO: uncomment test
    # (("methods", ("GET", "POST", "DELETE")),),  # TODO: uncomment test
    # (("methods", {"GET", "POST", "DELETE"}),),  # TODO: uncomment test
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
def test_load_config_with_valid_csrf_settings(
  csrf_settings: Tuple[Tuple[str, Union[None, bool, bytes, int, float, str]], ...],
) -> None:
  @CsrfProtect.load_config
  def _() -> Tuple[Tuple[str, Union[None, bool, bytes, int, float, str]], ...]:
    return csrf_settings
