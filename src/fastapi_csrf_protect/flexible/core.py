#!/usr/bin/env python3
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/src/fastapi_csrf_protect/flexible/core.py
# VERSION:     1.0.3
# CREATED:     2025-08-11 16:02:06+02:00
# AUTHOR:      Eliam Lotonga <e.m.lotonga@gmail.com>
# DESCRIPTION: https://www.w3docs.com/snippets/python/what-is-init-py-for.html
#
# HISTORY:
# *************************************************************

### Standard packages ###
from functools import partial
from typing import Tuple

### Third-party packages ###
from pydantic import ValidationError
from starlette.requests import Request

### Local modules ###
from fastapi_csrf_protect.exceptions import InvalidHeaderError, MissingTokenError
from fastapi_csrf_protect.flexible.csrf_config import CsrfConfig


class CsrfProtect(CsrfConfig):
  """Flexible CSRF validation: accepts token from either header or form body.

  Priority:
    1. Header
    2. Body
  """

  async def get_csrf_from_request(self, request: Request) -> str | None:
    token: None | str = None
    extractors = [
      partial(self.get_csrf_from_headers, request.headers),
      partial(self.get_csrf_from_body, request),
    ]
    for extractor in extractors:
      try:
        token = extractor()
        if token:
          break
      except (InvalidHeaderError, MissingTokenError, ValidationError):
        continue
    # token = token or self.get_csrf_from_body(await request.body())
    if token is None:
      raise MissingTokenError("Token must be provided.")
    return token

  async def get_csrf_token(self, request: Request):
    return await self.get_csrf_from_request(request)


__all__: Tuple[str, ...] = ("CsrfProtect",)
