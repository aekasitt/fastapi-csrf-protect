#!/usr/bin/env python3
# Copyright (C) 2020-2024 All rights reserved.
# FILENAME:    ~~/src/fastapi_csrf_protect/exceptions.py
# VERSION:     1.0.0
# CREATED:     2020-11-25 14:35
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
class CsrfProtectError(Exception):
  def __init__(self, status_code: int, message: str):
    self.status_code = status_code
    self.message = message


class InvalidHeaderError(CsrfProtectError):
  def __init__(self, message: str):
    super().__init__(422, message)


class MissingTokenError(CsrfProtectError):
  def __init__(self, message: str):
    super().__init__(400, message)


class TokenValidationError(CsrfProtectError):
  def __init__(self, message: str):
    super().__init__(401, message)


__all__ = ("CsrfProtectError", "InvalidHeaderError", "MissingTokenError", "TokenValidationError")
