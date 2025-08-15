### Standard packages ###
from typing import Dict, Optional, Tuple

### Third-party packages ###
from fastapi.testclient import TestClient
from httpx import Response, URL
from pytest import mark

### Local modules ###
from . import test_client
from fastapi_csrf_protect.flexible import CsrfProtect


@mark.parametrize(
  "csrf_settings,test_client",
  (
    (
      (("cookie_secure", True), ("secret_key", "secret")),
      "flexible",
    ),
    (
      (
        ("cookie_samesite", "lax"),
        ("cookie_secure", True),
        ("secret_key", "secret"),
      ),
      "flexible",
    ),
    (
      (
        ("cookie_samesite", "none"),
        ("cookie_secure", True),
        ("secret_key", "secret"),
      ),
      "flexible",
    ),
    (
      (
        ("cookie_samesite", "strict"),
        ("cookie_secure", True),
        ("secret_key", "secret"),
      ),
      "flexible",
    ),
  ),
  ids=(
    "cookie-headers-secure",
    "cookie-headers-samesite-lax-secure",
    "cookie-headers-samesite-none-secure",
    "cookie-headers-samesite-strict-secure",
  ),
  indirect=["test_client"],
)
def test_submit_csrf_token_in_headers_or_body_and_cookie_secure(
  csrf_settings: Tuple[Tuple[str, str], ...], test_client: TestClient
) -> None:
  ### Bypass TestClient base_url to https for `Secure` cookies ###
  test_client.base_url = URL("https://testserver")

  ### Load config ###
  @CsrfProtect.load_config
  def _() -> Tuple[Tuple[str, str], ...]:
    return csrf_settings

  ### Generate token ###
  response: Response = test_client.get("/gen-token")
  assert response.status_code == 200

  ### Asserts that `cookie_token` is present
  cookie_token: Optional[str] = test_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is not None

  ### Extract `csrf_token` from response to be set as next request's header ###
  csrf_token: Optional[str] = response.json().get("csrf_token", None)
  assert csrf_token is not None
  headers: Dict[str, str] = {"X-CSRF-Token": csrf_token}

  ### Post to protected endpoint ###
  response = test_client.post("/protected", headers=headers)

  ### Assertions ###
  csrf_token = response.json().get("fastapi-csrf-token")
  assert csrf_token is None
  assert response.status_code == 200
  assert response.json() == {"detail": "OK"}
  cookie_token = test_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is None

  ### Immediately get protected contents again ###
  response = test_client.post("/protected", headers=headers)

  ### Assertions ###
  assert response.status_code == 400
  assert response.json() == {"detail": "Missing Cookie: `fastapi-csrf-token`."}


@mark.parametrize(
  "csrf_settings,test_client",
  (
    ((("secret_key", "secret"), ("token_key", "csrf-token")), "flexible"),
    (
      (
        ("cookie_samesite", "lax"),
        ("secret_key", "secret"),
        ("token_key", "csrf-token"),
      ),
      "flexible"
    ),
    (
      (
        ("cookie_samesite", "strict"),
        ("secret_key", "secret"),
        ("token_key", "csrf-token"),
      ),
      "flexible"
    )
  ),
  ids=("cookie-body", "cookie-body-samesite-lax", "cookie-body-samesite-strict"),
  indirect=["test_client"],
)
def test_submit_csrf_token_in_body_and_cookies(
  csrf_settings: Tuple[Tuple[str, str], ...], test_client: TestClient
) -> None:
  ### Load config ###
  @CsrfProtect.load_config
  def _() -> Tuple[Tuple[str, str], ...]:
    return csrf_settings

  ### Generate token ###
  response: Response = test_client.get("/gen-token")
  assert response.status_code == 200

  ### Asserts that `cookie_token` is present
  cookie_token: Optional[str] = test_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is not None

  ### Extract `csrf_token` from response to be set as next request's body ###
  csrf_token: Optional[str] = response.json().get("csrf_token", None)
  payload: Dict[str, str] = {"csrf-token": csrf_token} if csrf_token is not None else {}

  ### Post to protected endpoint ###
  response = test_client.post("/protected", data=payload)

  ### Assertions ###
  assert response.status_code == 200
  assert response.json() == {"detail": "OK"}
  cookie_token = test_client.cookies.get("fastapi-csrf-token", None)
  assert cookie_token is None

  ### Immediately get protected contents again ###
  response = test_client.post("/protected", data=payload)

  ### Assertions ###
  assert response.status_code == 400
  assert response.json() == {"detail": "Missing Cookie: `fastapi-csrf-token`."}
