from fastapi.testclient import TestClient

from database.dao.user_dao import get_user_by_username
from main import app
from testing.helpers.generate_token import MOCK_TOKEN_BENJA, MOCK_TOKEN_JULI, MOCK_TOKEN_TONI, MOCK_TOKEN_VALEN
from utils.user_utils import *
from view_entities.user_view_entities import UserIDs

client = TestClient(app)

def test_inexistent_user():
    response = client.post(
        "/password-restore-request",
        json = {
            'username': 'inexistent',
            'email': 'inexistent',
        }
    )

    assert response.status_code == INEXISTENT_USERNAME_EMAIL_COMBINATION.status_code
    assert response.json()["detail"] == INEXISTENT_USERNAME_EMAIL_COMBINATION.detail

    response = client.post(
        "/password-restore-request",
        json = {
            'username': 'inexistent',
            'email': 'basbenja3@gmail.com',
        }
    )

    assert response.status_code == INEXISTENT_USERNAME_EMAIL_COMBINATION.status_code
    assert response.json()["detail"] == INEXISTENT_USERNAME_EMAIL_COMBINATION.detail

    response = client.post(
        "/password-restore-request",
        json = {
            'username': 'bas_benja',
            'email': 'inexistent',
        }
    )

    assert response.status_code == INEXISTENT_USERNAME_EMAIL_COMBINATION.status_code
    assert response.json()["detail"] == INEXISTENT_USERNAME_EMAIL_COMBINATION.detail

    response = client.post(
        "/password-restore-request",
        json = {
            'username': 'juliolcese',
            'email': 'basbenja3@gmail.com',
        }
    )

    assert response.status_code == INEXISTENT_USERNAME_EMAIL_COMBINATION.status_code
    assert response.json()["detail"] == INEXISTENT_USERNAME_EMAIL_COMBINATION.detail


def test_not_verified_user():
    response = client.post(
        "/password-restore-request",
        json = {
            'username': 'valennegrelli',
            'email': 'valen57negrelli@yahoo.com.ar',
        }
    )

    assert response.status_code == NOT_VERIFIED_EXCEPTION.status_code
    assert response.json()["detail"] == NOT_VERIFIED_EXCEPTION.detail


def test_successful_request():
    response = client.post(
        "/password-restore-request",
        json = {
            'username': 'bas_benja',
            'email': 'basbenja3@gmail.com',
        }
    )

    assert response.status_code == status.HTTP_200_OK


def test_successful_request():
    response = client.post(
        "/password-restore-request",
        json = {
            'username': 'pyrobots',
            'email': 'pyrobots.notreply@gmail.com',
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert get_user_by_username('pyrobots').restore_password_code != None