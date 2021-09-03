#!/usr/bin/env python3
# Copyright (C) 2019-2020 All rights reserved.
# FILENAME:  fastapi_csrf_config.py
# VERSION: 	 0.1.7
# CREATED: 	 2020-11-25 14:35
# AUTHOR: 	 Aekasitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
from typing import Callable, List, Sequence
from pydantic import ValidationError
from fastapi_csrf_protect.load_config import LoadConfig

class CsrfConfig(object):
  _csrf_header_name: str          = 'X-CSRF-Token'
  _csrf_header_type: str          = None
  _csrf_in_cookies: bool          = True
  _csrf_methods: Sequence[str]    = { 'POST', 'PUT', 'PATCH', 'DELETE' }
  _max_age: int                   = 3600
  _secret_key: str                = None
  _token_locations: Sequence[str] = { 'headers' }
  # In case of using cookies
  _cookie_key: str                = 'fastapi-csrf-token'
  _cookie_path: str               = '/'
  _cookie_domain: str             = None
  _cookie_secure: bool            = False
  _cookie_samesite: bool          = None
  _cookie_csrf_protect: bool      = True
  _httponly: bool                 = True

  @property
  def token_in_headers(self) -> bool:
    return 'headers' in self._token_locations

  @property
  def token_in_cookies(self) -> bool:
    return 'cookies' in self._token_locations

  @classmethod
  def load_config(cls, settings: Callable[..., List[tuple]]) -> 'CsrfConfig':
    try:
      config = LoadConfig(**{key.lower():value for key,value in settings()})
      cls._csrf_header_name = config.csrf_header_name
      cls._csrf_header_type = config.csrf_header_type
      cls._csrf_in_cookies = config.csrf_in_cookies
      cls._csrf_methods = config.csrf_methods
      cls._max_age = config.max_age
      cls._secret_key = config.secret_key
      cls._token_locations = config.token_locations
      cls._cookie_key = config.cookie_key
      cls._cookie_path = config.cookie_path
      cls._cookie_domain = config.cookie_domain
      cls._cookie_secure = config.cookie_secure
      cls._cookie_samesite = config.cookie_samesite
      cls._cookie_csrf_protect = config.cookie_csrf_protect
      cls._httponly = config.httponly
    except ValidationError: raise
    except Exception:
      raise TypeError('CsrfConfig must be pydantic "BaseSettings" or list of tuple')