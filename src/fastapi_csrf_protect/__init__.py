#!/usr/bin/env python3
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/src/fastapi_csrf_protect/__init__.py
# VERSION:     1.0.2
# CREATED:     2020-11-25 14:35
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION: https://www.w3docs.com/snippets/python/what-is-init-py-for.html
#
# HISTORY:
# *************************************************************
"""
FastAPI extension that provides Csrf Protection Token support
"""

### Standard packages ###
from typing import Any, Callable, ClassVar, Optional, Sequence, Tuple

### Third-party packages ###
from starlette.datastructures import Headers
from starlette.requests import Request
from starlette.responses import Response

### Local modules ###
from fastapi_csrf_protect.core import CsrfProtect as CsrfProtectImpl

class CsrfProtect:
  impl: ClassVar[CsrfProtectImpl] = CsrfProtectImpl()

  @classmethod
  def load_config(cls, settings: Callable[..., Sequence[Tuple[str, Any]]]) -> None:
    cls.impl.load_config(settings)

  def generate_csrf_tokens(self, secret_key: Optional[str] = None) -> Tuple[str, str]:
    return self.impl.generate_csrf_tokens(secret_key)

  def get_csrf_from_body(self, data: bytes) -> str:
    return self.impl.get_csrf_from_body(data)

  def get_csrf_from_headers(self, headers: Headers) -> str:
    return self.impl.get_csrf_from_headers(headers)

  def set_csrf_cookie(self, csrf_signed_token: str, response: Response) -> None:
    self.impl.set_csrf_cookie(csrf_signed_token, response)

  def unset_csrf_cookie(self, response: Response) -> None:
    self.impl.unset_csrf_cookie(response)

  async def validate_csrf(
    self,
    request: Request,
    cookie_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    time_limit: Optional[int] = None,
  ) -> None:
    await self.impl.validate_csrf(request, cookie_key, secret_key, time_limit)


__all__: Tuple[str, ...] = ("CsrfProtect",)
__name__ = "fastapi-csrf-protect"
__package__ = "fastapi-csrf-protect"
__version__ = "1.0.2"
