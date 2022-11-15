from fastapi.testclient import TestClient

from main import app
from testing.helpers.mock_db import MOCK_AVATAR

client = TestClient(app)


# Try logging in with inexistent username
def test_inexistent_user():
    response = client.post(
        '/login',
        json = {
            'username_or_email': 'basbenja3',
            'password': 'password'
        }
    )

    assert response.status_code == 401
    assert response.json() == {
        'detail': 'Inexistent user.'
    }


# Try logging in with wrong password
def test_invalid_credentials():
    response = client.post(
        '/login',
        json = {
            'username_or_email': 'sebagiraudo',
            'password': 'password'
        }
    )

    assert response.status_code == 401
    assert response.json() == {
        'detail': 'Invalid credentials.'
    }


# Not verified user tries to log in
def test_not_verified_user():
    response = client.post(
        '/login',
        json = {
            'username_or_email': 'israangulo4',
            'password': 'Argentiña222'
        }
    )

    assert response.status_code == 401
    assert response.json() == {
        'detail': 'Not verified user.'
    }


# Logging in with username and correct password
# Get token in return
def test_login_username():
    response = client.post(
        '/login',
        json = {
            'username_or_email': 'bas_benja',
            'password': 'Compuamigos2'
        }
    )

    assert response.status_code == 200
    assert response.json()['authorization'] != ''
    assert response.json()['avatar'] == MOCK_AVATAR


# Logging in with email and correct password
# Get token in return
def test_login_email():
    response = client.post(
        '/login',
        json = {
            'username_or_email': 'valen57negrelli@yahoo.com.ar',
            'password': 'piXies18'
        }
    )

    assert response.status_code == 200
    assert response.json()['authorization'] != ''
    assert response.json()['avatar'] == ''