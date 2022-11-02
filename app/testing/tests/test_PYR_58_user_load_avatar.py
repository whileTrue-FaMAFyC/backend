from fastapi.testclient import TestClient
import requests
import os

from main import app
from database.dao.user_dao import *


client = TestClient(app)


def test_successful_load_not_default_avatar():
    response = client.post(
        f"/load-avatar/lucasca22ina",
        files = {
            'avatar': ('avatar2.png', open('../avatar2.png', 'rb'), 'image/png' )
        }
    )

    assert response.status_code == 200
    assert os.path.exists('../assets/users/lucasca22ina/avatar.png') == True
    assert get_user_by_username("lucasca22ina").avatar == '../assets/users/lucasca22ina/avatar.png'
    os.remove('../assets/users/lucasca22ina/avatar.png')
    os.rmdir('../assets/users/lucasca22ina/')


def test_successful_load_default_avatar():
    response = client.post(
        f"/load-avatar/lucasca22ina",
    )

    assert response.status_code == 200
    assert get_user_by_username("lucasca22ina").avatar == 'default'


def test_user_not_registered():
    response = client.post(
        f"/load-avatar/totomondejar",
        files = {
            'avatar': ('avatar2.png', open('../avatar2.png', 'rb'), 'image/png' )
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "User not registered."


def test_user_not_verified():
    response = client.post(
        f"/load-avatar/tonimondejar",
        files = {
            'avatar': ('avatar2.png', open('../avatar2.png', 'rb'), 'image/png' )
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not verified user."

def test_avatar_already_loaded():
    response = client.post(
        f"/load-avatar/bas_benja",
        files = {
            'avatar': ('avatar2.png', open('../avatar2.png', 'rb'), 'image/png' )
        }
    )

    assert response.status_code == 403
    # Must fail because the avatar was already loaded (it is "fake_avatar(username")
    assert response.json()["detail"] == "Avatar already loaded."

    assert get_user_by_username("bas_benja").avatar == '../assets/users/bas_benja/avatar.png'


def test_avatar_format_not_valid():
    response = client.post(
        f"/load-avatar/lucasca22ina",
        files = {
            'avatar': ('avatar2.png', open('../avatar2.png', 'rb'), 'video/png' )
        }
    )

    assert response.status_code == 415
    assert response.json()["detail"] == "Avatar extension file not supported."
