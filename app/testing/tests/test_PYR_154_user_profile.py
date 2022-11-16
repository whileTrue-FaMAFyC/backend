from fastapi.testclient import TestClient

from main import app
from testing.helpers.generate_token import MOCK_TOKEN_BENJA
from testing.helpers.mock_db import MOCK_AVATAR
from utils.user_utils import INVALID_TOKEN_EXCEPTION


client = TestClient(app)

def test_successful_profile():
    response = client.get(
        "/user-profile",
        headers = {"Authorization": MOCK_TOKEN_BENJA}
    )
    
    assert response.status_code == 200
    assert response.json() == {
        "username": "bas_benja", 
        "email": "basbenja3@gmail.com"
    }
    return

def test_invalid_token():
    response = client.get(
        "/user-profile",
        headers = {"Authorization": ""}
    )

    assert response.status_code == INVALID_TOKEN_EXCEPTION.status_code
    assert response.json()["detail"] == INVALID_TOKEN_EXCEPTION.detail