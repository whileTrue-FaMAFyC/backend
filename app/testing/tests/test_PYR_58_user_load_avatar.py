from fastapi.testclient import TestClient

from database.dao.user_dao import *
from main import app
from testing.helpers.mock_db import MOCK_AVATAR

client = TestClient(app)

def test_successful_load_not_default_avatar():
    response = client.post(
        "/load-avatar/lucasca22ina",
        json={"avatar": "data:image/png;not_default"}
    )

    assert response.status_code == 200

    assert get_user_by_username("lucasca22ina").avatar == "data:image/png;not_default"


def test_successful_load_default_avatar():
    response = client.post(
        "/load-avatar/lucasca22ina",
        json={"avatar": ""}
    )

    assert response.status_code == 200

    assert get_user_by_username("lucasca22ina").avatar == "default"


def test_user_not_registered():
    response = client.post(
        "/load-avatar/totomondejar",
        json={"avatar": "fake_default"}
    )

    assert response.status_code == 401

    # Must fail because the username does not exist in the database
    assert response.json()["detail"] == "User not registered."


def test_user_not_verified():
    response = client.post(
        "/load-avatar/tonimondejar",
        json={"avatar": "fake_default"}
    )

    assert response.status_code == 401

    # Must fail because the user is not verified.
    assert response.json()["detail"] == "Not verified user."

def test_avatar_already_loaded():
    response = client.post(
        "/load-avatar/bas_benja",
        json={"avatar": "fake_default"}
    )

    assert response.status_code == 403
    # Must fail because the avatar was already loaded (it is "fake_avatar")
    assert response.json()["detail"] == "Avatar already loaded."

    assert get_user_by_username("bas_benja").avatar == MOCK_AVATAR


def test_avatar_format_not_valid():
    response = client.post(
        "/load-avatar/lucasca22ina",
        json={"avatar": "data:python-x/fake_default"}
    )

    assert response.status_code == 415
    # Must fail because the avatar was already loaded (it is "fake_avatar")
    assert response.json()["detail"] == "Avatar extension file not supported."
