#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/examples/header.py
# VERSION:     1.0.6
# CREATED:     2023-05-23 16:56
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from minijinja import Environment
from os import path
from pydantic_settings import BaseSettings
from typing import Annotated


def loader(name):
  segments: list[str] = []
  for segment in name.split("/"):
    if "\\" in segment or segment in (".", ".."):
      return None
    segments.append(segment)
  try:
    with open(path.join("templates", *segments)) as file:
      return file.read()
  except (IOError, OSError):
    pass


app = FastAPI()
environment = Environment(loader=loader, reload_before_render=True)


class CsrfSettings(BaseSettings):
  secret_key: str = "asecrettoeverybody"
  cookie_samesite: str = "none"
  cookie_secure: bool = True


@CsrfProtect.load_config
def get_csrf_config():
  return CsrfSettings()


@app.get("/", response_class=HTMLResponse)
async def form(
  request: Request, csrf_protect: Annotated[CsrfProtect, Depends(CsrfProtect)]
) -> HTMLResponse:
  """
  Returns form template.
  """
  csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
  content = environment.render_template("header.html", csrf_token=csrf_token, request=request)
  response = HTMLResponse(content=content)
  csrf_protect.set_csrf_cookie(signed_token, response)
  return response


@app.post("/login", response_class=JSONResponse)
async def login(request: Request, csrf_protect: CsrfProtect = Depends()):
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
