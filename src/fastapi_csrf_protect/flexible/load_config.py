#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/src/fastapi_csrf_protect/flexible/load_config.py
# VERSION:     1.0.7
# CREATED:     2025-08-11 16:02:06+02:00
# AUTHOR:      Eliam Lotonga <e.m.lotonga@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from __future__ import annotations
from typing import Literal, Optional, Set

### Third-party packages ###
from pydantic import (
  BaseModel,
  StrictBool,
  StrictInt,
  StrictStr,
  model_validator,
)


class LoadConfig(BaseModel):
  """Same as the base LoadConfig, but no token_location & token_key validations."""

  cookie_key: Optional[StrictStr] = "fastapi-csrf-token"
  cookie_path: Optional[StrictStr] = "/"
  cookie_domain: Optional[StrictStr] = None
  cookie_samesite: Optional[Literal["lax", "none", "strict"]] = "lax"
  cookie_secure: Optional[StrictBool] = False
  header_name: Optional[StrictStr] = "X-CSRF-Token"
  header_type: Optional[StrictStr] = None
  httponly: Optional[StrictBool] = True
  max_age: Optional[StrictInt] = 3600
  methods: Optional[Set[Literal["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]]] = None
  secret_key: Optional[StrictStr] = None

  @model_validator(mode="after")
  def validate_cookie_samesite_none_secure(self) -> LoadConfig:
    if self.cookie_samesite in {None, "none"} and self.cookie_secure is not True:
      raise ValueError('The "cookie_secure" must be True if "cookie_samesite" set to "none".')
    return self


__all__: tuple[str, ...] = ("LoadConfig",)
