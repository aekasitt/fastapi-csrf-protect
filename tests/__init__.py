#!/usr/bin/env python3
# Copyright (C) 2019-2020 All rights reserved.
# FILENAME:  tests/__init__.py
# VERSION: 	 0.2.0
# CREATED: 	 2020-11-26 18:50
# AUTHOR: 	 Aekasitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from pytest import fixture
### Third-Party Packages ###
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
### Local Modules ###
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError

@fixture
def setup() -> TestClient:
  app = FastAPI()
  @app.get('/set-cookie')
  def cookie(csrf_protect: CsrfProtect = Depends()):
    response = JSONResponse(status_code=200, content={'detail': 'OK'})
    csrf_protect.set_csrf_cookie(response)
    return response
  @app.get('/protected')
  def protected(request: Request, csrf_protect: CsrfProtect = Depends()):
    csrf_protect.validate_csrf_in_cookies(request)
    return JSONResponse(status_code=200, content={'detail': 'OK'})
  @app.exception_handler(CsrfProtectError)
  def csrf_protect_error_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(status_code=exc.status_code, content={'detail': exc.message})
  return TestClient(app)
