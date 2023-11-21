#!/usr/bin/env python3
# Copyright (C) 2021-2023 All rights reserved.
# FILENAME:  load_config.py
# VERSION: 	 0.3.3
# CREATED: 	 2020-11-25 14:35
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
from typing import Any, Dict, Optional, Set
from pydantic import BaseModel, validator, StrictBool, StrictInt, StrictStr


class LoadConfig(BaseModel):
    cookie_key: Optional[StrictStr] = "fastapi-csrf-token"
    cookie_path: Optional[StrictStr] = "/"
    cookie_domain: Optional[StrictStr] = None
    # NOTE: `cookie_secure` must be placed before `cookie_samesite`
    cookie_secure: Optional[StrictBool] = False
    cookie_samesite: Optional[StrictStr] = "lax"
    header_name: Optional[StrictStr] = "X-CSRF-Token"
    header_type: Optional[StrictStr] = None
    httponly: Optional[StrictBool] = True
    max_age: Optional[StrictInt] = 3600
    methods: Optional[Set[StrictStr]] = {"POST", "PUT", "PATCH", "DELETE"}
    secret_key: Optional[StrictStr] = None
    token_location: Optional[StrictStr] = "header"
    token_key: Optional[StrictStr] = None

    @validator("methods", each_item=True)
    def validate_csrf_methods(cls, value):
        if value.upper() not in {"GET", "HEAD", "POST", "PUT", "DELETE", "PATCH"}:
            raise ValueError('The "csrf_methods" must be between http request methods')
        return value.upper()

    @validator("cookie_samesite", always=True)
    def validate_cookie_samesite(cls, value: str, values: Dict[str, Any]):
        if value not in {"strict", "lax", "none"}:
            raise ValueError(
                'The "cookie_samesite" must be between "strict", "lax", or "none".'
            )
        elif value == "none" and values.get("cookie_secure", False) is not True:
            raise ValueError(
                'The "cookie_secure" must be True if "cookie_samesite" set to "none".'
            )
        return value

    @validator("token_location")
    def validate_token_location(cls, value: str):
        if value not in {"body", "header"}:
            raise ValueError('The "token_location" must be either "body" or "header".')
        return value

    @validator("token_key", always=True)
    def validate_token_key(cls, value: Optional[str], values: Dict[str, Any]):
        token_location: str = values.get("token_location", "header")
        if token_location == "body" and value is None:
            raise ValueError(
                'The "token_key" must be present when "token_location" is "body"'
            )
        return value
