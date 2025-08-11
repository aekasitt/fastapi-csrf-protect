#!/usr/bin/env python3
# Copyright (C) 2020-2025 All rights reserved.
# FILENAME:    ~~/src/fastapi_csrf_protect/core.py
# VERSION:     1.0.3
# CREATED:     2020-11-25 14:35
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
from functools import partial
### Standard packages ###
from hashlib import sha1
from re import match
from os import urandom
from typing import Dict, Optional, Tuple, Union, Callable, Sequence, Any

### Third-party packages ###
from itsdangerous import BadData, SignatureExpired, URLSafeTimedSerializer
from pydantic import create_model, ValidationError
from pydantic_settings import BaseSettings
from starlette.datastructures import Headers, UploadFile
from starlette.requests import Request
from starlette.responses import Response

### Local modules ###
from fastapi_csrf_protect.csrf_config import CsrfConfig
from fastapi_csrf_protect.exceptions import (
  InvalidHeaderError,
  MissingTokenError,
  TokenValidationError,
)


class CsrfProtect:
  csrf_config: CsrfConfig = CsrfConfig()

  @classmethod
  def load_config(cls, settings: Callable[..., Union[Sequence[Tuple[str, Any]], BaseSettings]]):
    cls.csrf_config.load_config(settings)

  def generate_csrf_tokens(self, secret_key: Optional[str] = None) -> Tuple[str, str]:
    """
    Generate a CSRF token and a signed CSRF token using server's secret key to be stored in cookie.

    ---
    :param secret_key: (Optional) the secret key used when generating tokens for users
    :type secret_key: (str | None) Defaults to None.
    """
    secret_key = secret_key or self.csrf_config._secret_key
    if secret_key is None:
      raise RuntimeError("A secret key is required to use CsrfProtect extension.")
    serializer = URLSafeTimedSerializer(secret_key, salt="fastapi-csrf-token")
    token = sha1(urandom(64)).hexdigest()
    signed = serializer.dumps(token)
    return token, signed

  def get_csrf_from_body(self, data: bytes) -> str:
    """
    Get token from the request body

    ---
    :param data: attached request body containing cookie data with configured `token_key`
    :type data: bytes
    """
    fields: Dict[str, Tuple[type, str]] = {self.csrf_config._token_key: (str, "csrf-token")}
    Body = create_model("Body", **fields)
    content: str = '{"' + data.decode("utf-8").replace("&", '","').replace("=", '":"') + '"}'
    body = Body.model_validate_json(content)
    token: str = body.model_dump()[self.csrf_config._token_key]
    return token

  def get_csrf_from_headers(self, headers: Headers) -> str:
    """
    Get token from the request headers

    ---
    :param headers: Headers containing header with configured `header_name`
    :type headers: starlette.datastructures.Headers
    """
    header_name, header_type = self.csrf_config._header_name, self.csrf_config._header_type
    header_parts = None
    try:
      header_parts = headers[header_name].split()
    except KeyError:
      raise InvalidHeaderError(f'Bad headers. Expected "{header_name}" in headers')
    token = None
    # Make sure the header is in a valid format that we are expecting, ie
    if not header_type:
      # <HeaderName>: <Token>
      if len(header_parts) != 1:
        raise InvalidHeaderError(f'Bad {header_name} header. Expected value "<Token>"')
      token = header_parts[0]
    else:
      # <HeaderName>: <HeaderType> <Token>
      if not match(r"{}\s".format(header_type), headers[header_name]) or len(header_parts) != 2:
        raise InvalidHeaderError(
          f'Bad {header_name} header. Expected value "{header_type} <Token>"'
        )
      token = header_parts[1]
    return token

  def get_csrf_from_form(self, request: Request) -> str | None:
    token = request._json.get(self.csrf_config._token_key, "") if hasattr(request, "_json") else None

    if not token and hasattr(request, "_form") and request._form is not None:
      form_data: Union[None, UploadFile, str] = request._form.get(self.csrf_config._token_key)
      if not form_data or isinstance(form_data, UploadFile):
        raise MissingTokenError("Form data must be of type string")
      token = form_data
    return token

  async def get_csrf_token(self, request: Request):
    if self.csrf_config._token_location == "header":
      return self.get_csrf_from_headers(request.headers)

    token = self.get_csrf_from_form(request)
    if token is None:
      token = self.get_csrf_from_body(await request.body())

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
      self.csrf_config._cookie_key,
      csrf_signed_token,
      max_age=self.csrf_config._max_age,
      path=self.csrf_config._cookie_path,
      domain=self.csrf_config._cookie_domain,
      secure=self.csrf_config._cookie_secure,
      httponly=self.csrf_config._httponly,
      samesite=self.csrf_config._cookie_samesite,
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
      self.csrf_config._cookie_key,
      path=self.csrf_config._cookie_path,
      domain=self.csrf_config._cookie_domain,
      secure=self.csrf_config._cookie_secure,
      httponly=self.csrf_config._httponly,
      samesite=self.csrf_config._cookie_samesite,
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
    secret_key = secret_key or self.csrf_config._secret_key
    if secret_key is None:
      raise RuntimeError("A secret key is required to use CsrfProtect extension.")
    cookie_key = cookie_key or self.csrf_config._cookie_key
    signed_token = request.cookies.get(cookie_key)
    if signed_token is None:
      raise MissingTokenError(f"Missing Cookie: `{cookie_key}`.")

    token = await self.get_csrf_token(request)

    self._validate_csrf_token(token, signed_token, time_limit=time_limit, secret_key=secret_key)

  def _validate_csrf_token(self, token: str, signed_token: str, *, secret_key: str |None=None, time_limit: int|None=None) -> None:
    time_limit = time_limit or self.csrf_config._max_age

    serializer = URLSafeTimedSerializer(secret_key, salt="fastapi-csrf-token")
    try:
      signature: str = serializer.loads(signed_token, max_age=time_limit)
      if token != signature:
        raise TokenValidationError("The CSRF signatures submitted do not match.")
    except SignatureExpired:
      raise TokenValidationError("The CSRF token has expired.")
    except BadData:
      raise TokenValidationError("The CSRF token is invalid.")


__all__: Tuple[str, ...] = ("CsrfProtect",)
