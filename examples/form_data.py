#!/usr/bin/env python3
# Copyright (C) 2020-2024 All rights reserved.
# FILENAME:    ~~/examples/form_data.py
# VERSION:     1.0.0
# CREATED:     2023-11-04 14:50
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from pydantic import EmailStr, StrictStr
from pydantic_settings import BaseSettings

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class CsrfSettings(BaseSettings):
  secret_key: str = "asecrettoeverybody"
  cookie_samesite: str = "none"
  cookie_secure: bool = True
  token_location: str = "body"
  token_key: str = "csrf-token"


@CsrfProtect.load_config
def get_csrf_config():
  return CsrfSettings()


@app.get("/")
async def form(request: Request, csrf_protect: CsrfProtect = Depends()):
  """
  Returns form template.
  """
  csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
  response = templates.TemplateResponse("form.html", {"request": request, "csrf_token": csrf_token})
  csrf_protect.set_csrf_cookie(signed_token, response)
  return response


@app.post("/login", response_class=JSONResponse)
async def login(
  request: Request,
  email: EmailStr = Form(),
  name: StrictStr = Form(),
  password: StrictStr = Form(),
  csrf_protect: CsrfProtect = Depends(),
) -> JSONResponse:
  """
  Login using form data
  """
  await csrf_protect.validate_csrf(request)
  response: JSONResponse = JSONResponse(status_code=200, content={"detail": "OK"})
  csrf_protect.unset_csrf_cookie(response)  # prevent token reuse
  return response


@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(_: Request, exc: CsrfProtectError):
  return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
