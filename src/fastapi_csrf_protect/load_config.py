#!/usr/bin/env python3
# Copyright (C) 2020-2024 All rights reserved.
# FILENAME:    ~~/src/fastapi_csrf_protect/load_config.py
# VERSION:     0.3.5
# CREATED:     2020-11-25 14:35
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
from typing import Any, Dict, Literal, Optional, Set
from pydantic import (
  BaseModel,
  Field,
  StrictBool,
  StrictInt,
  StrictStr,
  ValidationInfo,
  field_validator,
  model_validator,
)


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
  methods: Optional[Set[Literal["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]]] = Field(
    {"DELETE", "PATCH", "POST", "PUT"}, validate_default=True
  )
  secret_key: Optional[StrictStr] = None
  token_location: Optional[StrictStr] = "header"
  token_key: Optional[StrictStr] = None

  @field_validator("cookie_samesite")
  def validate_cookie_samesite(cls, value: str, info: ValidationInfo) -> str:
    values: Dict[str, Any] = dict(info.data.values())
    if value not in {"strict", "lax", "none"}:
      raise ValueError('The "cookie_samesite" must be between "strict", "lax", or "none".')
    elif value == "none" and values.get("cookie_secure", False) is not True:
      raise ValueError('The "cookie_secure" must be True if "cookie_samesite" set to "none".')
    return value

  @field_validator("token_location")
  def validate_token_location(cls, value: str):
    if value not in {"body", "header"}:
      raise ValueError('The "token_location" must be either "body" or "header".')
    return value

  @model_validator(mode="after")
  def validate_token_key(self, _: ValidationInfo) -> "LoadConfig":
    token_location: str = self.token_location if self.token_location is not None else "header"
    if token_location == "body":
      if self.token_key is None:
        raise ValueError('The "token_key" must be present when "token_location" is "body"')
    return self


__all__ = ("LoadConfig",)
