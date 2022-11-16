from fastapi.testclient import TestClient

from main import app
from testing.helpers.generate_token import *
from database.dao.user_dao import get_user_by_username
from utils.user_utils import verify_password

client = TestClient(app)

def correct_log_in(username: str, password: str):
    # Log in with the current password
    response = client.post(
        '/login',
        json = {
            'username_or_email': username,
            'password': password
        }
    )

    assert response.status_code == 200
    assert response.json()['Authorization'] != ''


def incorrect_log_in(username: str, password: str):
    # Log in with the current password
    response = client.post(
        '/login',
        json = {
            'username_or_email': username,
            'password': password
        }
    )

    assert response.status_code == 401
    assert response.json() == {
        'detail': 'Invalid credentials.'
    }


# Try changing the password with wrong current password
def test_invalid_credentials():
    response = client.patch(
        '/change-password',
        headers = {"Authorization": MOCK_TOKEN_BENJA},
        json = {
            'current_password': 'thisIsNotTheRightPassword',
            'new_password': 'NewPassword25',
            'new_password_confirmation':  'NewPassword25'
        }
    )
    
    assert response.status_code == 401
    assert response.json() == {
        'detail': 'Invalid credentials.'
    }
    
    incorrect_log_in('bas_benja', 'NewPassword25')
    correct_log_in('bas_benja', 'Compuamigos2')
    
    
# Try changing the password with new password that doesn't have the right format
def test_new_password_format_not_valid():
    response = client.patch(
        '/change-password',
        headers = {"Authorization": MOCK_TOKEN_BENJA},
        json = {
            'current_password': 'Compuamigos2',
            'new_password': 'notcapitalletters',
            'new_password_confirmation': 'notcapitalletters'
        }
    )
    
    assert response.status_code == 400
    assert response.json() == {
        'detail': 'Password format not valid.'
    }
    
    incorrect_log_in('bas_benja', 'notcapitalletters')
    correct_log_in('bas_benja', 'Compuamigos2')

  
# New password and its confirmation don't match
def test_new_password_dont_match():
    response = client.patch(
        '/change-password',
        headers = {"Authorization": MOCK_TOKEN_JULI},
        json = {
            'current_password': '1whileTrue1',
            'new_password': 'RightFormat1',
            'new_password_confirmation': 'dontmatch'
        }
    )
    
    assert response.status_code == 400
    assert response.json() == {
        'detail': "Password and password confirmation don't match."
    }
    
    incorrect_log_in('juliolcese', 'RightFormat1')
    correct_log_in('juliolcese', '1whileTrue1')


# New password is the same as the current one
def test_new_password_same_as_current():
    response = client.patch(
        '/change-password',
        headers = {"Authorization": MOCK_TOKEN_JULI},
        json = {
            'current_password': '1whileTrue1',
            'new_password': '1whileTrue1',
            'new_password_confirmation': '1whileTrue1'
        }
    )
    
    assert response.status_code == 400
    assert response.json() == {
        'detail': "New password is the same as the current one."
    }

    correct_log_in('juliolcese', '1whileTrue1')


# Successful password change
def test_successful_password_change():
    response = client.patch(
        '/change-password',
        headers = {"Authorization": MOCK_TOKEN_JULI},
        json = {
            'current_password': '1whileTrue1',
            'new_password': 'NewPassword1',
            'new_password_confirmation': 'NewPassword1'
        }
    )

    assert response.status_code == 200
    assert verify_password(
        'NewPassword1', 
        get_user_by_username('juliolcese').hashed_password
    ) == True
    
    incorrect_log_in('juliolcese', '1whileTrue1')
    correct_log_in('juliolcese', 'NewPassword1')
    