#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/tests/flexible/load_config.py
# VERSION:     1.0.7
# CREATED:     2025-08-11 16:02:06+02:00
# AUTHOR:      Eliam Lotonga <e.m.lotonga@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Union

### Third-party packages ###
from pydantic import ValidationError
from pytest import mark, raises

### Local modules ###
from fastapi_csrf_protect.flexible import CsrfProtect


@mark.parametrize(
  "csrf_settings, reason",
  (
    (
      (("cookie_samesite", None),),
      '1 validation error for LoadConfig\n  Value error, The "cookie_secure" must be True if "cookie_samesite" set to "none"',
    ),
    (
      (("cookie_samesite", "none"),),
      '1 validation error for LoadConfig\n  Value error, The "cookie_secure" must be True if "cookie_samesite" set to "none"',
    ),
    ((("cookie_samesite", b"lax"),), "1 validation error for LoadConfig\ncookie_samesite\n"),
    ((("cookie_samesite", b"none"),), "1 validation error for LoadConfig\ncookie_samesite\n"),
    ((("cookie_samesite", b"strict"),), "1 validation error for LoadConfig\ncookie_samesite\n"),
    ((("cookie_samesite", "null"),), "1 validation error for LoadConfig\ncookie_samesite\n"),
    ((("cookie_samesite", b"null"),), "1 validation error for LoadConfig\ncookie_samesite\n"),
    ((("cookie_samesite", 0),), "1 validation error for LoadConfig\ncookie_samesite\n"),
    ((("cookie_samesite", 1),), "1 validation error for LoadConfig\ncookie_samesite\n"),
    ((("cookie_samesite", True),), "1 validation error for LoadConfig\ncookie_samesite\n"),
    ((("cookie_samesite", False),), "1 validation error for LoadConfig\ncookie_samesite\n"),
    ((("cookie_samesite", 2.0),), "1 validation error for LoadConfig\ncookie_samesite\n"),
    ((("cookie_samesite", {1, 2, 3}),), "1 validation error for LoadConfig\ncookie_samesite\n"),
    (
      (("cookie_samesite", {1.0, 2.0, 3.0}),),
      "1 validation error for LoadConfig\ncookie_samesite\n",
    ),
    (
      (("cookie_samesite", {"1", "2", "3"}),),
      "1 validation error for LoadConfig\ncookie_samesite\n",
    ),
    (
      (("cookie_samesite", [1, 2, 3]),),
      "1 validation error for LoadConfig\ncookie_samesite\n",
    ),
    (
      (("cookie_samesite", [1.0, 2.0, 3.0]),),
      "1 validation error for LoadConfig\ncookie_samesite\n",
    ),
    (
      (("cookie_samesite", ["1", "2", "3"]),),
      "1 validation error for LoadConfig\ncookie_samesite\n",
    ),
    (
      (("cookie_samesite", {"key": "value"}),),
      "1 validation error for LoadConfig\ncookie_samesite\n",
    ),
    ((("cookie_secure", "false"),), "1 validation error for LoadConfig\ncookie_secure\n"),
    ((("cookie_secure", b"true"),), "1 validation error for LoadConfig\ncookie_secure\n"),
    ((("header_name", 2),), "1 validation error for LoadConfig\nheader_name\n"),
    ((("header_name", 1.0),), "1 validation error for LoadConfig\nheader_name\n"),
    ((("header_name", True),), "1 validation error for LoadConfig\nheader_name\n"),
    ((("header_name", b"header_name"),), "1 validation error for LoadConfig\nheader_name\n"),
    ((("header_name", []),), "1 validation error for LoadConfig\nheader_name\n"),
    ((("header_name", {}),), "1 validation error for LoadConfig\nheader_name\n"),
    ((("header_type", 2),), "1 validation error for LoadConfig\nheader_type\n"),
    ((("header_type", 1.0),), "1 validation error for LoadConfig\nheader_type\n"),
    ((("header_type", True),), "1 validation error for LoadConfig\nheader_type\n"),
    (
      (("header_type", b"header_type"),),
      "1 validation error for LoadConfig\nheader_type\n",
    ),
    ((("header_type", []),), "1 validation error for LoadConfig\nheader_type\n"),
    ((("header_type", {}),), "1 validation error for LoadConfig\nheader_type\n"),
    ((("httponly", "false"),), "1 validation error for LoadConfig\nhttponly\n"),
    ((("httponly", b"true"),), "1 validation error for LoadConfig\nhttponly\n"),
    ((("methods", 2),), "1 validation error for LoadConfig\nmethods\n"),
    ((("methods", 1.0),), "1 validation error for LoadConfig\nmethods\n"),
    ((("methods", True),), "1 validation error for LoadConfig\nmethods\n"),
    ((("methods", b"GET, POST"),), "1 validation error for LoadConfig\nmethods\n"),
    ((("methods", "GET, POST"),), "1 validation error for LoadConfig\nmethods\n"),
    ((("methods", {}),), "1 validation error for LoadConfig\nmethods\n"),
    ((("methods", [1, 2, 3]),), "3 validation errors for LoadConfig"),
    ((("methods", (1, 2, 3)),), "3 validation errors for LoadConfig"),
    ((("methods", {1, 2, 3}),), "3 validation errors for LoadConfig"),
    (
      (("methods", ["1", "2", "3"]),),
      "3 validation errors for LoadConfig",
    ),
    (
      (("methods", ("1", "2", "3")),),
      "3 validation errors for LoadConfig",
    ),
    (
      (("methods", {"1", "2", "3"}),),
      "3 validation errors for LoadConfig",
    ),
    (
      (("methods", {"key": "value"}),),
      "1 validation error for LoadConfig\nmethods\n",
    ),
    ((("secret_key", 2),), "1 validation error for LoadConfig\nsecret_key\n"),
    ((("secret_key", 1.0),), "1 validation error for LoadConfig\nsecret_key\n"),
    ((("secret_key", True),), "1 validation error for LoadConfig\nsecret_key\n"),
    ((("secret_key", b"secret"),), "1 validation error for LoadConfig\nsecret_key\n"),
    ((("secret_key", []),), "1 validation error for LoadConfig\nsecret_key\n"),
    ((("secret_key", {}),), "1 validation error for LoadConfig\nsecret_key\n"),
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
    "methods-list-1-2-3",
    "methods-tuple-1-2-3",
    "methods-list-1-2-3-as-strings",
    "methods-tuple-1-2-3-as-strings",
    "methods-set-1-2-3-as-strings",
    "methods-dict-key-value",
    "secret-key-2",
    "secret-key-1.0",
    "secret-key-True",
    "secret-key-secret-as-bytes",
    "secret-key-empty-list",
    "secret-key-empty-set",
    "token-location-body-without-token-key",
  ],
)
def test_load_config_with_invalid_csrf_settings(
  csrf_settings: tuple[tuple[str, Union[None, bool, bytes, float, int, str]], ...], reason: str
) -> None:
  with raises(ValidationError) as exc_info:

    @CsrfProtect.load_config
    def _() -> tuple[tuple[str, Union[None, bool, bytes, int, float, str]], ...]:
      return csrf_settings

  assert exc_info is not None
  assert str(exc_info.value).startswith(reason)


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
    (("methods", {"GET", "POST", "DELETE"}),),
    (("methods", ("GET", "POST", "DELETE")),),
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
  ids=(
    "header_name-header_name",
    "header_type-header_type",
    "httponly-False",
    "httponly-None",
    "httponly-True",
    "methods-empty-list",
    "methods-list-GET-POST-DELETE",
    "methods-set-GET-POST-DELETE",
    "methods-tuple-GET-POST-DELETE",
    "secret_key-secret",
    "token_location-body-token_key-csrf-token",
    "token_location-header",
    "cookie_samesite-None-cookie_secure-True",
    "cookie_samesite-lax",
    "cookie_samesite-none-cookie_secure-True",
    "cookie_samesite-strict",
    "cookie_secure-False",
    "cookie_secure-None",
    "cookie_secure-True",
  ),
)
def test_load_config_with_valid_csrf_settings(
  csrf_settings: tuple[tuple[str, Union[None, bool, bytes, int, float, str]], ...],
) -> None:
  @CsrfProtect.load_config
  def _() -> tuple[tuple[str, Union[None, bool, bytes, int, float, str]], ...]:
    return csrf_settings
