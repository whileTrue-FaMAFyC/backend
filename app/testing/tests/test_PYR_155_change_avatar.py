from fastapi.testclient import TestClient

from database.dao.user_dao import *
from main import app
from testing.helpers.generate_token import MOCK_TOKEN_BENJA
from utils.user_utils import AVATAR_NOT_INSERTED, AVATAR_FORMAT_NOT_VALID

client = TestClient(app)


def test_avatar_format_not_valid():
    response = client.put(
        "/change-avatar",
        headers={'Authorization': MOCK_TOKEN_BENJA},
        json={"avatar": "data:python-x/fake_default"}
    )

    assert response.status_code == AVATAR_FORMAT_NOT_VALID.status_code
    # Must fail because the avatar was already loaded (it is "fake_avatar")
    assert response.json()["detail"] == AVATAR_FORMAT_NOT_VALID.detail


def test_avatar_not_inserted():
    response = client.put(
        "/change-avatar",
        headers={'Authorization': MOCK_TOKEN_BENJA},
        json={"avatar": ""}
    )

    assert response.status_code == 400

    assert response.json()["detail"] == AVATAR_NOT_INSERTED.detail


def test_successful_change_avatar():
    response = client.put(
        "/change-avatar",
        headers={'Authorization': MOCK_TOKEN_BENJA},
        json={"avatar": "data:image/png;fakeavatar"}
    )

    assert response.status_code == 200

    assert get_user_by_username(
        "bas_benja").avatar == "data:image/png;fakeavatar"
