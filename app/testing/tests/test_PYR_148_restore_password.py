from fastapi.testclient import TestClient

from database.dao.user_dao import get_user_by_username
from main import app
from testing.helpers.generate_token import MOCK_TOKEN_BENJA, MOCK_TOKEN_JULI, MOCK_TOKEN_TONI, MOCK_TOKEN_VALEN
from utils.user_utils import *
from view_entities.user_view_entities import UserIDs

client = TestClient(app)

def test_inexistent_user():
    response = client.put(
        "/password-restore",
        json = {
            'email': 'inexistent',
            'new_password': 'NewPass123',
            'restore_password_code': '123456'
        }
    )

    assert response.status_code == USER_NOT_REGISTERED.status_code
    assert response.json()["detail"] == USER_NOT_REGISTERED.detail

def test_not_verified_user():
    response = client.put(
        "/password-restore",
        json = {
            'email': 'valen57negrelli@yahoo.com.ar',
            'new_password': 'NewPass123',
            'restore_password_code': '123456'
        }
    )

    assert response.status_code == NOT_VERIFIED_EXCEPTION.status_code
    assert response.json()["detail"] == NOT_VERIFIED_EXCEPTION.detail


def test_invalid_restore_code():
    response = client.put(
        "/password-restore",
        json = {
            'email': 'pyrobots.notreply@gmail.com',
            'new_password': 'NewPass123',
            'restore_password_code': '123456'
        }
    )

    assert response.status_code == INVALID_RESTORE_CODE.status_code
    assert response.json()["detail"] == INVALID_RESTORE_CODE.detail

    response = client.post(
        "/password-restore-request",
        json = {
            'username': 'pyrobots',
            'email': 'pyrobots.notreply@gmail.com',
        }
    )

    user = get_user_by_username('pyrobots')
    original_code = user.restore_password_code

    assert response.status_code == status.HTTP_200_OK
    assert original_code != None

    incorrect_code =  original_code + 1

    response = client.put(
        "/password-restore",
        json = {
            'email': 'pyrobots.notreply@gmail.com',
            'new_password': 'NewPass123',
            'restore_password_code': incorrect_code
        }
    )

    assert response.status_code == INVALID_RESTORE_CODE.status_code
    assert response.json()["detail"] == INVALID_RESTORE_CODE.detail
    assert get_user_by_username('pyrobots').restore_password_code == original_code


def test_invalid_password_format():

    response = client.post(
        "/password-restore-request",
        json = {
            'username': 'pyrobots',
            'email': 'pyrobots.notreply@gmail.com',
        }
    )

    user = get_user_by_username('pyrobots')
    restore_code = user.restore_password_code

    assert response.status_code == status.HTTP_200_OK
    assert restore_code != None

    response = client.put(
        "/password-restore",
        json = {
            'email': 'pyrobots.notreply@gmail.com',
            'new_password': 'invalidpass',
            'restore_password_code': restore_code
        }
    )

    assert response.status_code == PASSWORD_FORMAT_NOT_VALID.status_code
    assert response.json()["detail"] == PASSWORD_FORMAT_NOT_VALID.detail
    assert get_user_by_username('pyrobots').restore_password_code == restore_code


def test_successful_restore():

    response = client.post(
        "/password-restore-request",
        json = {
            'username': 'pyrobots',
            'email': 'pyrobots.notreply@gmail.com',
        }
    )

    user = get_user_by_username('pyrobots')
    restore_code = user.restore_password_code

    assert response.status_code == status.HTTP_200_OK
    assert restore_code != None

    new_password = 'NewPass123'
    response = client.put(
        "/password-restore",
        json = {
            'email': 'pyrobots.notreply@gmail.com',
            'new_password': new_password,
            'restore_password_code': restore_code
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert get_user_by_username('pyrobots').restore_password_code == 0
    assert get_user_by_username('pyrobots').hashed_password != new_password

    response = client.post(
        '/login',
        json = {
            'username_or_email': 'pyrobots.notreply@gmail.com',
            'password': 'NewPass123'
        }
    )

    assert response.status_code == 200
    assert response.json()['Authorization'] != ''