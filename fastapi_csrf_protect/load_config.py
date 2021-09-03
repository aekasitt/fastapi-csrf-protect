#!/usr/bin/env python3
# Copyright (C) 2019-2020 All rights reserved.
# FILENAME:  load_config.py
# VERSION: 	 0.1.6
# CREATED: 	 2020-11-25 14:35
# AUTHOR: 	 Aekasitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
from typing import Optional, Sequence
from pydantic import BaseModel, validator, StrictBool, StrictInt, StrictStr

class LoadConfig(BaseModel):
  csrf_header_name:Optional[StrictStr] = 'X-CSRF-Token'
  csrf_header_type:Optional[StrictStr] = None
  csrf_in_cookies:Optional[StrictBool] = True
  csrf_methods:Optional[Sequence[StrictStr]] = { 'POST', 'PUT', 'PATCH', 'DELETE' }
  max_age:Optional[StrictInt] = 3600
  secret_key:Optional[StrictStr] = None
  token_locations:Optional[Sequence[StrictStr]] = { 'headers' }
  # In case of using cookies
  cookie_key:Optional[StrictStr] = 'fastapi-csrf-token'
  cookie_path:Optional[StrictStr] = '/'
  cookie_domain:Optional[StrictStr] = None
  cookie_secure:Optional[StrictBool] = False
  cookie_samesite:Optional[StrictStr] = None
  cookie_csrf_protect:Optional[StrictBool] = True
  httponly:Optional[StrictBool] = True

  @validator('csrf_methods', each_item=True)
  def validate_csrf_methods(cls, value):
    if value.upper() not in {'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'PATCH'}:
      raise ValueError('The "csrf_methods" must be between http request methods')
    return value.upper()

  @validator('cookie_samesite')
  def validate_cookie_samesite(cls, value):
    if value not in ['strict', 'lax', 'none']:
      raise ValueError('The "cookie_samesite" must be between "strict", "lax", "none"')
    return value
