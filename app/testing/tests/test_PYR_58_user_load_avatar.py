from fastapi.testclient import TestClient
import os
from PIL import Image
import io

from app import USERS_ASSETS
from database.dao.user_dao import *
from main import app

def mock_avatar():
    return ('avatar2.png', open('./testing/helpers/avatar2.png', 'rb'), 'image/png' )

client = TestClient(app)


def test_successful_load_not_default_avatar():
    response = client.post(
        f"/load-avatar/lucasca22ina",
        files = {
            'avatar': mock_avatar()
        }
    )

    assert response.status_code == 200
    assert os.path.exists(f'{USERS_ASSETS}/lucasca22ina/avatar.png') == True
    assert get_user_by_username("lucasca22ina").avatar == f'{USERS_ASSETS}/lucasca22ina/avatar.png'
    
    # response = client.get(
    #     f'{USERS_ASSETS}/lucasca22ina/avatar.png'
    # )
    
    # image = Image.open(io.BytesIO(response.content))
    # image.show()

    os.remove(f'{USERS_ASSETS}/lucasca22ina/avatar.png')
    os.rmdir(f'{USERS_ASSETS}/lucasca22ina/')


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
            'avatar': mock_avatar()
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "User not registered."


def test_user_not_verified():
    response = client.post(
        f"/load-avatar/tonimondejar",
        files = {
            'avatar': mock_avatar()
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not verified user."

def test_avatar_already_loaded():
    response = client.post(
        f"/load-avatar/bas_benja",
        files = {
            'avatar': mock_avatar()
        }
    )

    assert response.status_code == 403
    # Must fail because the avatar was already loaded (it is "fake_avatar(username")
    assert response.json()["detail"] == "Avatar already loaded."

    assert get_user_by_username("bas_benja").avatar == f'{USERS_ASSETS}/bas_benja/avatar.png'


def test_avatar_format_not_valid():
    response = client.post(
        f"/load-avatar/lucasca22ina",
        files = {
            'avatar': ('avatar2.png', open('./testing/helpers/avatar2.png', 'rb'), 'video/png' )
        }
    )

    assert response.status_code == 415
    assert response.json()["detail"] == "Avatar extension file not supported."
