import requests
import os

from database.dao.user_dao import *
from testing.helpers.mock_db import MOCK_AVATAR


URL = 'http://localhost:8000/load-avatar/'


def test_successful_load_not_default_avatar():
    response = requests.post(
        f"{URL}lucasca22ina",
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
    response = requests.post(
        f"{URL}lucasca22ina",
    )

    assert response.status_code == 200
    assert get_user_by_username("lucasca22ina").avatar == ''


def test_user_not_registered():
    response = requests.post(
        f"{URL}totomondejar",
        files = {
            'avatar': ('avatar2.png', open('../avatar2.png', 'rb'), 'image/png' )
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "User not registered."


def test_user_not_verified():
    response = requests.post(
        f"{URL}tonimondejar",
        files = {
            'avatar': ('avatar2.png', open('../avatar2.png', 'rb'), 'image/png' )
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not verified user."

# def test_avatar_already_loaded():
#     response = client.post(
#         "/load-avatar/bas_benja",
#         json={"avatar": "fake_default"}
#     )

#     assert response.status_code == 403
#     # Must fail because the avatar was already loaded (it is "fake_avatar")
#     assert response.json()["detail"] == "Avatar already loaded."

#     assert get_user_by_username("bas_benja").avatar == MOCK_AVATAR


# def test_avatar_format_not_valid():
#     response = client.post(
#         "/load-avatar/lucasca22ina",
#         json={"avatar": "data:python-x/fake_default"}
#     )

#     assert response.status_code == 415
#     # Must fail because the avatar was already loaded (it is "fake_avatar")
#     assert response.json()["detail"] == "Avatar extension file not supported."
