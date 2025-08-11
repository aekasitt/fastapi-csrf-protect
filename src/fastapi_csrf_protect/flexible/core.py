from functools import partial

from starlette.requests import Request
from pydantic import ValidationError

from fastapi_csrf_protect.core import CsrfProtect as BaseCsrfProtect
from fastapi_csrf_protect.exceptions import InvalidHeaderError, MissingTokenError
from fastapi_csrf_protect.flexible.csrf_config import CsrfConfig


class CsrfProtect(BaseCsrfProtect):
  """Flexible CSRF validation: accepts token from either header or form body.

    Priority:
      1. Header
      2. Body
  """
  _csrf_config: CsrfConfig = CsrfConfig()

  async def get_csrf_from_request(self, request: Request) -> str | None:
    token = None
    extractors = [
      partial(self.get_csrf_from_headers, request.headers),
      partial(self.get_csrf_from_form, request),
    ]

    for extractor in extractors:
      try:
        token = extractor()
        if token:
          break
      except (InvalidHeaderError, MissingTokenError, ValidationError):
        continue

    token = token or self.get_csrf_from_body(await request.body())
    if token is None:
      raise MissingTokenError("Token must be provided.")
    return token

  async def get_csrf_token(self, request: Request):
    return await self.get_csrf_from_request(request)
