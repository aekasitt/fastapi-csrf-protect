#!/usr/bin/env python3
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/tests/__init__.py
# VERSION:     1.0.0
# CREATED:     2020-11-26 18:50
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from pytest import fixture

### Third-party packages ###
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

### Local modules ###
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError


@fixture
def test_client() -> TestClient:
  """
  Sets up a FastAPI TestClient wrapped around an App implementing Context/Headers extension pattern

  ---
  :returns: TestClient
  """
  app = FastAPI()

  @app.get("/gen-token", response_class=JSONResponse)
  def generate(csrf_protect: CsrfProtect = Depends()):
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
    response: JSONResponse = JSONResponse(
      status_code=200, content={"detail": "OK", "csrf_token": csrf_token}
    )
    csrf_protect.set_csrf_cookie(signed_token, response)
    return response

  @app.get("/protected", response_class=JSONResponse)
  async def protected(request: Request, csrf_protect: CsrfProtect = Depends()):
    await csrf_protect.validate_csrf(request)
    response: JSONResponse = JSONResponse(status_code=200, content={"detail": "OK"})
    csrf_protect.unset_csrf_cookie(response)  # prevent token reuse
    return response

  @app.exception_handler(CsrfProtectError)
  def csrf_protect_error_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

  return TestClient(app)
