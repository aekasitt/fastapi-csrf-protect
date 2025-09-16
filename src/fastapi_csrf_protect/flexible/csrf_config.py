#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/src/fastapi_csrf_protect/flexible/csrf_config.py
# VERSION:     1.0.7
# CREATED:     2025-08-11 16:02:06+02:00
# AUTHOR:      Eliam Lotonga <e.m.lotonga@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Any, ClassVar, Callable, Literal, Optional, Sequence, Set, Union

### Third-party packages ###
from pydantic_settings import BaseSettings

### Local modules ###
from fastapi_csrf_protect.load_config import LoadConfig


class CsrfConfig(object):
  _cookie_key: ClassVar[str] = "fastapi-csrf-token"
  _cookie_path: ClassVar[str] = "/"
  _cookie_domain: ClassVar[Optional[str]] = None
  _cookie_samesite: ClassVar[Optional[Literal["lax", "strict", "none"]]] = None
  _cookie_secure: ClassVar[bool] = False
  _header_name: ClassVar[str] = "X-CSRF-Token"
  _header_type: ClassVar[Optional[str]] = None
  _httponly: ClassVar[bool] = True
  _max_age: ClassVar[int] = 3600
  _methods: ClassVar[Set[Literal["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]]] = {
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
  }
  _secret_key: ClassVar[Optional[str]] = None
  _token_key: ClassVar[str] = "csrf-token"

  @classmethod
  def load_config(
    cls, settings: Callable[..., Union[Sequence[tuple[str, Any]], BaseSettings]]
  ) -> None:
    """Load flexible CsrfProtect configurations via decorated method

    ---
    :param settings: callable returning either sequence of key-value tuples or pydantic BaseSettings
    :type settings: Callable[..., BaseSettings | Sequence[tuple, Any]]
    :raises pydantic_core.ValidationError: in case of settings' attribute type mismatched
    """
    config = LoadConfig(**{key.lower(): value for key, value in settings()})
    cls._cookie_key = config.cookie_key or cls._cookie_key
    cls._cookie_path = config.cookie_path or cls._cookie_path
    cls._cookie_domain = config.cookie_domain
    cls._cookie_samesite = config.cookie_samesite
    cls._cookie_secure = False if config.cookie_secure is None else config.cookie_secure
    cls._header_name = config.header_name or cls._header_name
    cls._header_type = config.header_type
    cls._httponly = True if config.httponly is None else config.httponly
    cls._max_age = config.max_age or cls._max_age
    cls._methods = config.methods or cls._methods
    cls._secret_key = config.secret_key
    cls._token_key = config.token_key or cls._token_key


__all__: tuple[str, ...] = ("CsrfConfig",)
