#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2020-2026 All rights reserved.
# FILENAME:    ~~/examples/stateful.py
# VERSION:     1.0.7
# CREATED:     2026-06-29 13:18
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
from cachette import Cachette
from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from minijinja import Environment
from os import path
from pydantic import EmailStr, StrictStr
from pydantic_settings import BaseSettings
from typing import Annotated
from uuid import uuid4 as uuid


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
    token_location: str = "body"
    token_key: str = "csrf-token"


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()


@app.get("/", response_class=HTMLResponse)
async def form(
    request: Request,
    cachette: Annotated[Cachette, Depends(Cachette)],
    csrf_protect: Annotated[CsrfProtect, Depends(CsrfProtect)],
) -> HTMLResponse:
    """
    Returns form template.
    """
    session_id = request.cookies.get("session-id", None)
    csrf_token: str
    signed_token: str
    if not session_id:
        session_id = str(uuid())
        csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
        await cachette.put(f"{session_id}-csrf-token", csrf_token)
        await cachette.put(f"{session_id}-signed-token", signed_token)
    else:
        session_csrf = await cachette.fetch(f"{session_id}-csrf-token")
        session_signed = await cachette.fetch(f"{session_id}-signed-token")
        if not session_csrf or not session_signed:
            raise CsrfProtectError(500, "Unable to find user signed tokens")
        csrf_token, signed_token = session_csrf, session_signed
    content: str = environment.render_template(
        "form.html", csrf_token=csrf_token, request=request
    )
    response: HTMLResponse = HTMLResponse(content=content)
    response.set_cookie(
        "session-id",
        session_id,
        max_age=60,
        path=None,
        domain=None,
        secure=True,
        httponly=True,
        samesite="strict",
    )
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
    response = JSONResponse(status_code=200, content={"detail": "OK"})
    csrf_protect.unset_csrf_cookie(response)  # prevent token reuse
    return response


@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(_: Request, exc: CsrfProtectError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
