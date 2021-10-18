#!/usr/bin/env python3
# Copyright (C) 2019-2020 All rights reserved.
# FILENAME:  examples/cookies.py
# VERSION: 	 0.2.1
# CREATED: 	 2021-08-19 14:02
# AUTHOR: 	 Aekasitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory='templates')

class CsrfSettings(BaseModel):
  secret_key:str = 'asecrettoeverybody'

@CsrfProtect.load_config
def get_csrf_config():
  return CsrfSettings()

@app.get('/form')
def form(request: Request, csrf_protect:CsrfProtect = Depends()):
  '''
  Returns form template.
  '''
  response = templates.TemplateResponse('form.html', { 'request': request })
  csrf_protect.set_csrf_cookie(response)
  return response

@app.post('/posts', response_class=JSONResponse)
def create_post(request: Request, csrf_protect:CsrfProtect = Depends()):
  '''
  Creates a new Post
  '''
  csrf_protect.validate_csrf_in_cookies(request)
  # Do stuff

@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
  return JSONResponse(status_code=exc.status_code, content={ 'detail':  exc.message })