#!/usr/bin/env python3
# Copyright (C) 2021-2023 All rights reserved.
# FILENAME:  examples/login.py
# VERSION: 	 0.3.0
# CREATED: 	 2023-05-23 16:56
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class CsrfSettings(BaseModel):
    secret_key: str = "asecrettoeverybody"
    cookie_samesite: str = "none"
    cookie_secure: bool = True


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()


@app.get("/login")
def form(request: Request, csrf_protect: CsrfProtect = Depends()):
    """
    Returns form template.
    """
    csrf_token = csrf_protect.generate_csrf()
    response = templates.TemplateResponse(
        "form.html", {"request": request, "csrf_token": csrf_token}
    )
    csrf_protect.set_csrf_cookie(csrf_token, response)
    return response


@app.post("/login", response_class=JSONResponse)
def login(request: Request, csrf_protect: CsrfProtect = Depends()):
    """
    Login using form data
    """
    csrf_protect.validate_csrf(request)
    # Do stuff


@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(_: Request, exc: CsrfProtectError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
