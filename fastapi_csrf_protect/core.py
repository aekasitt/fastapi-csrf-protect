#!/usr/bin/env python3
# Copyright (C) 2021-2023 All rights reserved.
# FILENAME:  core.py
# VERSION: 	 0.3.1
# CREATED: 	 2020-11-25 14:35
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
import re
from os import urandom
from hashlib import sha1
from typing import Optional, Tuple
from fastapi.requests import Request
from fastapi.responses import Response
from starlette.datastructures import Headers
from itsdangerous import BadData, SignatureExpired, URLSafeTimedSerializer
from fastapi_csrf_protect.csrf_config import CsrfConfig
from fastapi_csrf_protect.exceptions import (
    InvalidHeaderError,
    MissingTokenError,
    TokenValidationError,
)
from warnings import warn


class CsrfProtect(CsrfConfig):
    def generate_csrf(self, secret_key: Optional[str] = None) -> Tuple[str, str]:
        """
        Deprecated. Please use `generate_csrf_tokens` method instead.

        ---
        :param secret_key: (Optional) the secret key used when generating tokens for users
        :type secret_key: (str | None) Defaults to None.
        """
        warn("This is deprecated; version=0.3.1", DeprecationWarning, stacklevel=2)
        return self.generate_csrf_tokens(secret_key)

    def generate_csrf_tokens(self, secret_key: Optional[str] = None) -> Tuple[str, str]:
        """
        Generate a CSRF token and a signed CSRF token using server's secret key to be stored in
        cookie. R

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

    def get_csrf_from_headers(self, headers: Headers) -> str:
        """
        Get token from the headers

        ---
        :param headers: Headers containing header with configured `header_name`
        :type headers: starlette.datastructures.Headers
        """
        header_name, header_type = self._header_name, self._header_type
        header_parts = None
        try:
            header_parts = headers[header_name].split()
        except KeyError:
            raise InvalidHeaderError(
                f'Bad headers. Expected "{header_name}" in headers'
            )
        token = None
        # Make sure the header is in a valid format that we are expecting, ie
        if not header_type:
            # <HeaderName>: <Token>
            if len(header_parts) != 1:
                raise InvalidHeaderError(
                    f'Bad {header_name} header. Expected value "<Token>"'
                )
            token = header_parts[0]
        else:
            # <HeaderName>: <HeaderType> <Token>
            if (
                not re.match(r"{}\s".format(header_type), headers[header_name])
                or len(header_parts) != 2
            ):
                raise InvalidHeaderError(
                    f'Bad {header_name} header. Expected value "{header_type} <Token>"'
                )
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
            self._cookie_key, path=self._cookie_path, domain=self._cookie_domain
        )

    def validate_csrf(
        self,
        request: Request,
        cookie_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        time_limit: Optional[int] = None,
    ):
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
        token: str = self.get_csrf_from_headers(request.headers)
        serializer = URLSafeTimedSerializer(secret_key, salt="fastapi-csrf-token")
        try:
            signature: str = serializer.loads(signed_token, max_age=time_limit)
            if token != signature:
                raise TokenValidationError(
                    "The CSRF signatures submitted do not match."
                )
        except SignatureExpired:
            raise TokenValidationError("The CSRF token has expired.")
        except BadData:
            raise TokenValidationError("The CSRF token is invalid.")
