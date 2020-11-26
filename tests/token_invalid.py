#!/usr/bin/env python3
# Copyright (C) 2019-2020 All rights reserved.
# FILENAME:  token_invalid.py
# VERSION: 	 0.0.1
# CREATED: 	 2020-11-26 16:14
# AUTHOR: 	 Aekasitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
import pytest
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import TokenValidationError

@pytest.fixture(scope='function')
def client():
    app = FastAPI()
    @app.get('/set-cookie')
    def cookie(csrf_protect: CsrfProtect = Depends()):
      response = JSONResponse(status_code=200, content={'detail': 'OK'})
      response.set_cookie(csrf_protect._cookie_key, 'invalid')
      return response
    @app.get('/protected')
    def protected(request: Request, csrf_protect: CsrfProtect = Depends()):
      csrf_protect.validate_csrf_in_cookies(request)
    @app.exception_handler(TokenValidationError)
    def token_validation_handler(request: Request, exc: TokenValidationError):
      return JSONResponse(status_code=exc.status_code, content={'detail': exc.message})
    return TestClient(app)

@pytest.mark.parametrize('route',['/protected'])
def test_token_invalid_request(client, route):
  @CsrfProtect.load_config
  def get_configs():
    return [('secret_key', 'secret')]
  response = client.get('/set-cookie')
  assert response.status_code == 200
  response = client.get(route, cookies=response.cookies)
  assert response.status_code == 401
  assert response.json() == {'detail': 'The CSRF token is invalid.'}