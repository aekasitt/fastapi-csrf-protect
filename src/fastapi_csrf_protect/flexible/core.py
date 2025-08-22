#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/src/fastapi_csrf_protect/flexible/core.py
# VERSION:     1.0.6
# CREATED:     2025-08-11 16:02:06+02:00
# AUTHOR:      Eliam Lotonga <e.m.lotonga@gmail.com>
# DESCRIPTION: https://www.w3docs.com/snippets/python/what-is-init-py-for.html
#
# HISTORY:
# *************************************************************
import json
### Standard packages ###
from hashlib import sha1
from http.client import HTTPException
from json import JSONDecodeError
from os import urandom
from re import match
from typing import Optional, Union

### Third-party packages ###
from itsdangerous import BadData, SignatureExpired, URLSafeTimedSerializer
from pydantic import create_model
from starlette.datastructures import Headers, UploadFile
from starlette.requests import Request
from starlette.responses import Response

### Local modules ###
from fastapi_csrf_protect.exceptions import (
  MissingTokenError,
  TokenValidationError,
)
from fastapi_csrf_protect.flexible.csrf_config import CsrfConfig


class CsrfProtect(CsrfConfig):
  """Flexible CSRF validation: accepts token from either header or form body.

  Priority:
    1. Header
    2. Body
  """

  def generate_csrf_tokens(self, secret_key: Optional[str] = None) -> tuple[str, str]:
    """
    Generate a CSRF token and a signed CSRF token using server's secret key to be stored in cookie.

    ---
    :param secret_key: (Optional) the secret key used when generating tokens for users
    :type secret_key: (str | None) Defaults to None.
    """
    secret_key = secret_key or self._secret_key
    if secret_key is None:
      raise RuntimeError("A secret key is required to use CsrfProtect extension.")
    serializer = URLSafeTimedSerializer(secret_key, salt="fastapi-csrf-token")
    token = sha1(urandom(64)).hexdigest()
    signed = serializer.dumps(token)
    return token, signed

  async def _get_request_body(self, request: Request) -> bytes:
    """Get the body of the request.

    Read the raw body of the request and re-inject it into the request._body so that
     it remains available for further processing.
     (e.g., request.json(), request.form()).

     :param request: The FastAPI/Starlette request object
     :return: The raw body of the request as a bytes.
    """
    request_body = await request.body()
    request._body = request_body
    return request_body

  async def get_csrf_from_request(self, request: Request) -> Optional[str]:
    """Get token from the request.

    The token can come either from JSON body or form-data body.

    ---
    :param request: The incoming request containing csrf token with configured `token_key`
    :type request: starlette.requests.Request
    :return: The extracted CSRF token, or None if not found
    """
    token = None
    body_byte = await self._get_request_body(request)

    try:
      json_data = json.loads(body_byte)
      return json_data.get(self._token_key, "")
    except JSONDecodeError:
      pass

    try:
      form_data = await request.form()
      token = form_data.get(self._token_key, None)
      if not token or not isinstance(form_data, UploadFile):
        token = None
    except HTTPException:
      pass

    return token

  def get_csrf_from_body(self, data: bytes) -> str:
    """
    Get token from the request body

    ---
    :param data: attached request body containing cookie data with configured `token_key`
    :type data: bytes
    """
    fields: dict[str, tuple[type, str]] = {self._token_key: (str, "csrf-token")}
    Body = create_model("Body", **fields)  # type: ignore[call-overload]
    content: str = '{"' + data.decode("utf-8").replace("&", '","').replace("=", '":"') + '"}'
    body = Body.model_validate_json(content)
    token: str = body.model_dump()[self._token_key]
    return token

  def get_csrf_from_headers(self, headers: Headers) -> Union[None, str]:
    """
    Get token from the request headers

    ---
    :param headers: Headers containing header with configured `header_name`
    :type headers: starlette.datastructures.Headers
    """
    header_name, header_type = self._header_name, self._header_type
    header_parts = None
    try:
      header_parts = headers[header_name].split()
    except KeyError:
      return None
    token: Union[None, str] = None
    if not header_type:
      # <HeaderName>: <Token>
      if len(header_parts) != 1:
        return token
      token = header_parts[0]
    else:
      # <HeaderName>: <HeaderType> <Token>
      if not match(r"{}\s".format(header_type), headers[header_name]) or len(header_parts) != 2:
        return token
      token = header_parts[1]
    return token

  def set_csrf_cookie(self, csrf_signed_token: str, response: Response) -> None:
    """
    Sets Csrf Protection token to the response cookies

    ---
    :param csrf_signed_token: signed CSRF token from `generate_csrf_token` method
    :type csrf_signed_token: str
    :param response: The FastAPI response object to sets the access cookies in.
    :type response: fastapi.responses.Response
    """
    if not isinstance(response, Response):
      raise TypeError("The response must be an object response FastAPI")
    response.set_cookie(
      self._cookie_key,
      csrf_signed_token,
      max_age=self._max_age,
      path=self._cookie_path,
      domain=self._cookie_domain,
      secure=self._cookie_secure,
      httponly=self._httponly,
      samesite=self._cookie_samesite,
    )

  def unset_csrf_cookie(self, response: Response) -> None:
    """
    Remove Csrf Protection token from the response cookies

    ---
    :param response: The FastAPI response object to delete the access cookies in.
    :type response: fastapi.responses.Response
    """
    if not isinstance(response, Response):
      raise TypeError("The response must be an object response FastAPI")
    response.delete_cookie(
      self._cookie_key,
      path=self._cookie_path,
      domain=self._cookie_domain,
      secure=self._cookie_secure,
      httponly=self._httponly,
      samesite=self._cookie_samesite,
    )

  async def validate_csrf(
    self,
    request: Request,
    cookie_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    time_limit: Optional[int] = None,
  ) -> None:
    """
    Check if the given data is a valid CSRF token. This compares the given
    signed token to the one stored in the session.

    ---
    :param request: incoming Request instance
    :type request: fastapi.requests.Request
    :param cookie_key: (Optional) field name for the CSRF token field stored in cookies
        Default is set in CsrfConfig when `load_config` was called;
    :type cookie_key: str
    :param secret_key: (Optional) secret key used to decrypt the token
        Default is set in CsrfConfig when `load_config` was called;
    :type secret_key: str
    :param time_limit: (Optional) Number of seconds that the token is valid.
        Default is set in CsrfConfig when `load_config` was called;
    :type time_limit: int
    :raises TokenValidationError: Contains the reason that validation failed.
    """
    secret_key = secret_key or self._secret_key
    if secret_key is None:
      raise RuntimeError("A secret key is required to use CsrfProtect extension.")
    cookie_key = cookie_key or self._cookie_key
    signed_token = request.cookies.get(cookie_key)
    if signed_token is None:
      raise MissingTokenError(f"Missing Cookie: `{cookie_key}`.")
    time_limit = time_limit or self._max_age
    token: Optional[str] = self.get_csrf_from_headers(request.headers)
    if not token:
      token = await self.get_csrf_from_request(request) or self.get_csrf_from_body(await request.body())
    serializer = URLSafeTimedSerializer(secret_key, salt="fastapi-csrf-token")
    try:
      signature: str = serializer.loads(signed_token, max_age=time_limit)
      if token != signature:
        raise TokenValidationError("The CSRF signatures submitted do not match.")
    except SignatureExpired:
      raise TokenValidationError("The CSRF token has expired.")
    except BadData:
      raise TokenValidationError("The CSRF token is invalid.")


__all__: tuple[str, ...] = ("CsrfProtect",)
