#!/usr/bin/env python3
# Copyright (C) 2019-2020 All rights reserved.
# FILENAME:  token_expired.py
# VERSION: 	 0.0.1
# CREATED: 	 2020-11-26 16:14
# AUTHOR: 	 Aekasitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
import pytest
from time import sleep
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import MissingTokenError

global delay
delay = 2

@pytest.fixture(scope='function')
def client():
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
    @app.exception_handler(MissingTokenError)
    def missing_token_handler(request: Request, exc: MissingTokenError):
      return JSONResponse(status_code=exc.status_code, content={'detail': exc.message})
    return TestClient(app)

@pytest.mark.parametrize('route',['/protected'])
def test_token_expired_requests(client, route):
  @CsrfProtect.load_config
  def get_configs():
    return [('secret_key', 'secret'), ('max_age', delay)]
  response = client.get('/set-cookie')
  assert response.status_code == 200
  response = client.get(route, cookies=response.cookies)
  assert response.status_code == 200
  assert response.json() == {'detail': 'OK'}
  sleep(delay)
  response = client.get(route, cookies=response.cookies)
  assert response.status_code == 400
  assert response.json() == {'detail': 'Missing Cookie fastapi-csrf-token'}
