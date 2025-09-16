#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/tests/flexible/__init__.py
# VERSION:     1.0.7
# CREATED:     2025-08-15 16:13
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION: https://www.w3docs.com/snippets/python/what-is-init-py-for.html
#
# HISTORY:
# *************************************************************

### Standard packages ###
from collections.abc import Generator
from typing import Annotated

### Third-party packages ###
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from pytest import fixture

### Local modules ###
from fastapi_csrf_protect.exceptions import CsrfProtectError
from fastapi_csrf_protect.flexible import CsrfProtect


@fixture
def flexible_client() -> Generator[TestClient, None, None]:
  """
  Sets up a FastAPI TestClient wrapped around an application implementing both
  Context and Headers extension pattern

  ---
  :return: test client fixture used for local testing
  :rtype: fastapi.testclient.TestClient
  """
  app: FastAPI = FastAPI()

  @app.get("/gen-token", response_class=JSONResponse)
  def read_resource(csrf_protect: Annotated[CsrfProtect, Depends(CsrfProtect)]) -> JSONResponse:
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
    response: JSONResponse = JSONResponse(
      status_code=200, content={"detail": "OK", "csrf_token": csrf_token}
    )
    csrf_protect.set_csrf_cookie(signed_token, response)
    return response

  @app.post("/protected", response_class=JSONResponse)
  async def update_resource(
    request: Request,
    csrf_protect: Annotated[CsrfProtect, Depends(CsrfProtect)],
  ) -> JSONResponse:
    await csrf_protect.validate_csrf(request)
    response: JSONResponse = JSONResponse(status_code=200, content={"detail": "OK"})
    csrf_protect.unset_csrf_cookie(response)  # prevent token reuse
    return response

  @app.exception_handler(CsrfProtectError)
  def csrf_protect_error_handler(request: Request, exc: CsrfProtectError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

  with TestClient(app) as client:
    yield client


__all__: tuple[str, ...] = ("flexible_client",)
