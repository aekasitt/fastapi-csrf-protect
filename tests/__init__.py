#!/usr/bin/env python3
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/tests/__init__.py
# VERSION:     1.0.1
# CREATED:     2020-11-26 18:50
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION: https://www.w3docs.com/snippets/python/what-is-init-py-for.html
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from pytest import fixture

### Local modules ###
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError


@fixture
def test_client() -> TestClient:
  """
  Sets up a FastAPI TestClient wrapped around an application implementing both
  Context and Headers extension pattern

  ---
  :return: test client fixture used for local testing
  :rtype: fastapi.testclient.TestClient
  """
  app = FastAPI()

  @app.get("/gen-token", response_class=JSONResponse)
  def read_resource(csrf_protect: CsrfProtect = Depends()):
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
    response: JSONResponse = JSONResponse(
      status_code=200, content={"detail": "OK", "csrf_token": csrf_token}
    )
    csrf_protect.set_csrf_cookie(signed_token, response)
    return response

  @app.post("/protected", response_class=JSONResponse)
  async def update_resource(request: Request, csrf_protect: CsrfProtect = Depends()):
    await csrf_protect.validate_csrf(request)
    response: JSONResponse = JSONResponse(status_code=200, content={"detail": "OK"})
    csrf_protect.unset_csrf_cookie(response)  # prevent token reuse
    return response

  @app.exception_handler(CsrfProtectError)
  def csrf_protect_error_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

  return TestClient(app)


__all__ = ("test_client",)
