#!/usr/bin/env python3
# Copyright (C) 2019-2020 All rights reserved.
# FILENAME:  core.py
# VERSION: 	 0.2.1
# CREATED: 	 2020-11-25 14:35
# AUTHOR: 	 Aekasitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
import re
from os import urandom
from hashlib import sha1
from typing import Optional
from fastapi.requests import Request
from fastapi.responses import Response
from starlette.datastructures import Headers
from itsdangerous import BadData, SignatureExpired, URLSafeTimedSerializer
from fastapi_csrf_protect.csrf_config import CsrfConfig
from fastapi_csrf_protect.exceptions import InvalidHeaderError, MissingTokenError, TokenValidationError

class CsrfProtect(CsrfConfig):

  def __init__(self, request: Request = None, response: Response = None):
    '''
    Retrieve response object if jwt in the cookie

    ---
    :param request: all incoming request  
    :type request: fastapi.requests.Request  
    :param response: response from endpoint  
    :type response: fastapi.responses.Response  
    '''
    if response and self.token_in_cookies:
      self._response = response

  def generate_csrf(self, secret_key: Optional[str] = None):
    '''
    Generate a CSRF token.
    TODO: The token should be cached for a request, so multiple
    calls to this function will generate the same token.

    ---
    :param secret_key: (Optional) the secret key used when generating a new token for users
    :type secret_key: str
    '''
    secret_key = secret_key or self._secret_key
    if secret_key is None: raise RuntimeError('A secret key is required to use CSRF.')
    serializer = URLSafeTimedSerializer(secret_key, salt='fastapi-csrf-token')
    token = serializer.dumps(sha1(urandom(64)).hexdigest())
    return token

  def get_csrf_from_headers(self, headers: Headers) -> str:
    '''
    Get token from the headers

    ---
    :param headers: Headers containing header with configured `csrf_header_name`
    :type headers: starlette.datastructures.Headers
    '''
    header_name, header_type = self._csrf_header_name, self._csrf_header_type
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
      if not re.match(r"{}\s".format(header_type), headers[header_name]) or len(header_parts) != 2:
        raise InvalidHeaderError(f'Bad {header_name} header. Expected value "{header_type} <Token>"')
      token = header_parts[1]
    return token

  def set_csrf_cookie(self, response: Optional[Response] = None) -> None:
    '''
    Sets Csrf Protection token to the response cookies

    ---
    :param response: The FastAPI response object to sets the access cookies in.
    :type response: fastapi.responses.Response
    '''
    if response and not isinstance(response,Response):
      raise TypeError('The response must be an object response FastAPI')
    response = response or self._response
    response.set_cookie(
      self._cookie_key,
      self.generate_csrf(self._secret_key),
      max_age=self._max_age,
      path=self._cookie_path,
      domain=self._cookie_domain,
      secure=self._cookie_secure,
      httponly=self._httponly,
      samesite=self._cookie_samesite
    )

  def unset_csrf_cookie(self, response: Optional[Response] = None) -> None:
    '''
    Remove Csrf Protection token from the response cookies

    ---
    :param response: (Optional) The FastAPI response object to delete the access cookies in.
    :type response: fastapi.responses.Response
    '''
    if response and not isinstance(response, Response):
      raise TypeError('The response must be an object response FastAPI')
    response = response or self._response
    response.delete_cookie(
      self._cookie_key,
      path=self._cookie_path,
      domain=self._cookie_domain
    )

  def validate_csrf(self, data, secret_key: Optional[str] = None, time_limit: Optional[int] = None):
    '''
    Check if the given data is a valid CSRF token. This compares the given
    signed token to the one stored in the session.

    ---
    :param data: The signed CSRF token to be checked.
    :type data: Any
    :param secret_key: (Optional) secret key used to decrypt the token
        Default is set in CsrfConfig when `load_config` was called;
    :type secret_key: str
    :param time_limit: (Optional) Number of seconds that the token is valid.
        Default is set in CsrfConfig when `load_config` was called;
    :type time_limit: int
    :raises TokenValidationError: Contains the reason that validation failed.
    '''
    secret_key = secret_key or self._secret_key
    if secret_key is None: raise RuntimeError('A secret key is required to use CSRF.')
    time_limit = time_limit or self._max_age
    if not data:
      raise TokenValidationError('The CSRF token is missing.')
    serializer = URLSafeTimedSerializer(secret_key, salt='fastapi-csrf-token')
    try:
      token = serializer.loads(data, max_age=time_limit)
    except SignatureExpired:
      raise TokenValidationError('The CSRF token has expired.')
    except BadData:
      raise TokenValidationError('The CSRF token is invalid.')

  def validate_csrf_in_cookies(self, request: Request, secret_key: Optional[str] = None, field_name: Optional[str] = None):
    '''
    Check if the given Request with its Cookies contains a valid CSRF token.  
    Once extracted, off-loads logic to `validate_csrf` method.  

    ---
    :param request: all incoming request  
    :type request: fastapi.requests.Request
    :param secret_key: (Optional) secret key used to decrypt the token
    :type secret_key: str
    :param field_name: (Optional)
        Default is set in CsrfConfig when `load_config` was called;
    :type field_name: str
    '''
    field_name = field_name or self._cookie_key
    cookie = request.cookies.get(field_name)
    if cookie is None: raise MissingTokenError(f'Missing Cookie {field_name}')
    self.validate_csrf(cookie, secret_key)
