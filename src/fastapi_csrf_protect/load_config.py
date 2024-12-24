#!/usr/bin/env python3
# Copyright (C) 2020-2024 All rights reserved.
# FILENAME:    ~~/src/fastapi_csrf_protect/load_config.py
# VERSION:     1.0.0
# CREATED:     2020-11-25 14:35
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Literal, Optional, Set

### Third-party packages ###
from pydantic import (
  BaseModel,
  Field,
  StrictBool,
  StrictInt,
  StrictStr,
  model_validator,
)


class LoadConfig(BaseModel):
  cookie_key: Optional[StrictStr] = "fastapi-csrf-token"
  cookie_path: Optional[StrictStr] = "/"
  cookie_domain: Optional[StrictStr] = None
  cookie_samesite: Optional[Literal["lax", "none", "strict"]] = "lax"
  cookie_secure: Optional[StrictBool] = False
  header_name: Optional[StrictStr] = "X-CSRF-Token"
  header_type: Optional[StrictStr] = None
  httponly: Optional[StrictBool] = True
  max_age: Optional[StrictInt] = 3600
  methods: Optional[Set[Literal["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]]] = Field(
    {"DELETE", "PATCH", "POST", "PUT"}, validate_default=True
  )
  secret_key: Optional[StrictStr] = None
  token_location: Optional[Literal["body", "header"]] = "header"
  token_key: Optional[StrictStr] = None

  @model_validator(mode="after")
  def validate_cookie_samesite_none_secure(self) -> "LoadConfig":
    if self.cookie_samesite in {None, "none"} and self.cookie_secure is not True:
      raise ValueError('The "cookie_secure" must be True if "cookie_samesite" set to "none".')
    return self

  @model_validator(mode="after")
  def validate_token_key(self) -> "LoadConfig":
    token_location: str = self.token_location if self.token_location is not None else "header"
    if token_location == "body":
      if self.token_key is None:
        raise ValueError('The "token_key" must be present when "token_location" is "body"')
    return self


__all__ = ("LoadConfig",)
