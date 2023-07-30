### Third-Party Packages ###
from . import test_client
from fastapi.testclient import TestClient

### Local Modules ###
from fastapi_csrf_protect import CsrfProtect


def test_correct_form_hidden_field_token(test_client: TestClient):
    ### Loads Config ###
    @CsrfProtect.load_config
    def get_configs():
        return [("secret_key", "secret")]

    ### Generate token ###
    response = test_client.get("/gen-token")

    ### Assertion ###
    assert response.status_code == 200

    ### Extract `csrf_token` from response to be set as next request's hidden form field ###
    csrf_token: str = response.json().get("csrf_token", None)

    ### Get protected contents ###
    response = test_client.post("/form", data={"csrf_token": csrf_token})

    ### Assertions ###
    assert response.status_code == 200
    assert response.json() == {"detail": "OK"}
