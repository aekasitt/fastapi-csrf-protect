#!/usr/bin/env python3
# Copyright (C) 2021-2023 All rights reserved.
# FILENAME:  load_config.py
# VERSION: 	 0.2.2
# CREATED: 	 2020-11-25 14:35
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
from typing import Optional, Sequence
from pydantic import BaseModel, validator, StrictBool, StrictInt, StrictStr

class LoadConfig(BaseModel):
  cookie_key: Optional[StrictStr]        = 'fastapi-csrf-token'
  cookie_path: Optional[StrictStr]       = '/'
  cookie_domain: Optional[StrictStr]     = None
  cookie_samesite: Optional[StrictStr]   = 'lax'
  cookie_secure: Optional[StrictBool]    = False
  header_name: Optional[StrictStr]       = 'X-CSRF-Token'
  header_type: Optional[StrictStr]       = None
  httponly: Optional[StrictBool]         = True
  max_age: Optional[StrictInt]           = 3600
  methods: Optional[Sequence[StrictStr]] = { 'POST', 'PUT', 'PATCH', 'DELETE' }
  secret_key: Optional[StrictStr]        = None

  @validator('methods', each_item=True)
  def validate_csrf_methods(cls, value):
    if value.upper() not in {'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'PATCH'}:
      raise ValueError('The "csrf_methods" must be between http request methods')
    return value.upper()

  @validator('cookie_samesite', always=True)
  def validate_cookie_samesite(cls, value: str, values: dict):
    if value not in { 'strict', 'lax', 'none' }:
      raise ValueError('The "cookie_samesite" must be between "strict", "lax", or "none".')
    elif value == 'none' and values.get('cookie_secure', False) is not True:
      raise ValueError('The "cookie_secure" must be True if "cookie_samesite" set to "none".')
    return value
