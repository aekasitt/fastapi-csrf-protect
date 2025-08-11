#!/usr/bin/env python3
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/src/fastapi_csrf_protect/load_config.py
# VERSION:     1.0.3
# CREATED:     2020-11-25 14:35
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Optional, List, Literal, Set, Tuple, Union, get_args, get_origin

### Third-party packages ###
from dataclasses import dataclass


@dataclass
class LoadConfig:
  cookie_key: Optional[str] = "fastapi-csrf-token"
  cookie_path: Optional[str] = "/"
  cookie_domain: Optional[str] = None
  cookie_samesite: Optional[str] = "lax"
  cookie_secure: Optional[bool] = False
  header_name: Optional[str] = "X-CSRF-Token"
  header_type: Optional[str] = None
  httponly: Optional[bool] = True
  max_age: Optional[int] = 3600
  methods: Optional[Set[Literal["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]]] = None
  secret_key: Optional[str] = None
  token_location: Optional[str] = "header"
  token_key: Optional[str] = None

  def __post_init__(self) -> None:
    self.validate_attribute_types()
    self.validate_cookie_samesite()
    self.validate_cookie_samesite_none_secure()
    self.validate_methods()
    self.validate_token_key()
    self.validate_token_location()

  def validate_attribute_types(self) -> None:
    for name, field_type in self.__annotations__.items():
      origin = get_origin(field_type)
      if origin == Union:
        types = get_args(field_type)
        typed: List[bool] = []
        for current_type in types:
          if get_origin(current_type) is None:
            typed.append(isinstance(getattr(self, name), current_type))
          else:
            subscripted = get_origin(current_type)
            typed.append(isinstance(getattr(self, name), subscripted))
            # TODO: subtypes
        if not any(typed):
          raise TypeError(f'Field "{name}" was not correctly assigned as "{field_type}".')
      elif not isinstance(getattr(self, name), field_type):
        current_type = type(getattr(self, name))
        raise TypeError(
          f'Field "{name}" was assigned by "{current_type}" instead of "{field_type}".'
        )

  def validate_methods(self) -> None:
    if self.methods is not None and isinstance(self.methods, set):
      for method in self.methods:
        if method not in {"DELETE", "GET", "PATCH", "POST", "PUT"}:
          raise TypeError(
            'Field "methods" must consist only of "DELETE", "GET", "PATCH", "POST", or "PUT".'
          )

  def validate_cookie_samesite(self) -> None:
    if self.cookie_samesite is not None and self.cookie_samesite not in {"lax", "none", "strict"}:
      raise TypeError(
        'Field "cookie_samesite" when present must be either "lax", "none", or "strict".'
      )

  def validate_cookie_samesite_none_secure(self) -> None:
    if self.cookie_samesite in {None, "none"} and self.cookie_secure is not True:
      raise TypeError('Field "cookie_secure" must be True if "cookie_samesite" set to "none".')

  def validate_token_key(self) -> None:
    token_location: str = self.token_location if self.token_location is not None else "header"
    if token_location == "body" and self.token_key is None:
      raise TypeError('Field "token_key" must be present when "token_location" is "body"')

  def validate_token_location(self) -> None:
    if self.token_location not in {"body", "header"}:
      raise TypeError('Field "token_location" must be either "body" or "header".')


__all__: Tuple[str, ...] = ("LoadConfig",)
