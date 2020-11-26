#!/usr/bin/env python3
# Copyright (C) 2019-2020 All rights reserved.
# FILENAME:  missing_token.py
# VERSION: 	 0.0.1
# CREATED: 	 2020-11-26 16:14
# AUTHOR: 	 Aekasitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
import pytest, os
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import MissingTokenError

@pytest.fixture(scope='function')
def client():
    app = FastAPI()
    @app.get('/protected')
    def protected(request: Request, csrf_protect: CsrfProtect = Depends()):
      csrf_protect.validate_csrf_in_cookies(request)
    @app.exception_handler(MissingTokenError)
    def missing_token_handler(request: Request, exc: MissingTokenError):
      return JSONResponse(status_code=exc.status_code, content={'detail': exc.message})
    return TestClient(app)

@pytest.mark.parametrize('route',['/protected'])
def test_missing_token_request(client, route):
  @CsrfProtect.load_config
  def get_secret_key():
    return [('secret_key', 'secret')]
  response = client.get(route)
  assert response.status_code == 400
  assert response.json() == {'detail': 'Missing Cookie fastapi-csrf-token'}