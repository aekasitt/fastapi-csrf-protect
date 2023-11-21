#!/usr/bin/env python3
# Copyright (C) 2021-2023 All rights reserved.
# FILENAME:  fastapi_csrf_config.py
# VERSION: 	 0.3.3
# CREATED: 	 2020-11-25 14:35
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
### Standard Packages ###
from typing import Callable, List, Literal, Optional, Sequence

### Third-Party Modules ###
from pydantic import ValidationError

### Local Modules ###
from fastapi_csrf_protect.load_config import LoadConfig


class CsrfConfig(object):
    _cookie_key: str = "fastapi-csrf-token"
    _cookie_path: str = "/"
    _cookie_domain: Optional[str] = None
    _cookie_samesite: Optional[Literal["lax", "strict", "none"]] = None
    _cookie_secure: bool = False
    _header_name: str = "X-CSRF-Token"
    _header_type: Optional[str] = None
    _httponly: bool = True
    _max_age: int = 3600
    _methods: Sequence[str] = {"POST", "PUT", "PATCH", "DELETE"}
    _secret_key: str = None
    _token_location: str = "header"
    _token_key: Optional[str] = None

    @classmethod
    def load_config(cls, settings: Callable[..., List[tuple]]) -> None:
        try:
            config = LoadConfig(**{key.lower(): value for key, value in settings()})
            cls._cookie_key = config.cookie_key
            cls._cookie_path = config.cookie_path
            cls._cookie_domain = config.cookie_domain
            cls._cookie_samesite = config.cookie_samesite
            cls._cookie_secure = config.cookie_secure
            cls._header_name = config.header_name
            cls._header_type = config.header_type
            cls._httponly = config.httponly
            cls._max_age = config.max_age
            cls._methods = config.methods
            cls._secret_key = config.secret_key
            cls._token_location = config.token_location
            cls._token_key = config.token_key
        except ValidationError:
            raise
        except Exception as err:
            print(err)
            raise TypeError(
                'CsrfConfig must be pydantic "BaseSettings" or list of tuple'
            )
