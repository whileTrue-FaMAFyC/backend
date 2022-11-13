from fastapi.testclient import TestClient

from main import app
from testing.helpers.generate_token import *
from database.dao.user_dao import get_user_by_username
from utils.user_utils import verify_password

client = TestClient(app)


# Try changing the password with wrong current password
def test_invalid_credentials():
    response = client.post(
        '/change-password',
        headers = {"Authorization": MOCK_TOKEN_VALEN},
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
    
# Try changing the password with new password that doesn't have the right format
def test_new_password_format_not_valid():
    response = client.post(
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
    
# New password and its confirmation don't match
def test_new_password_dont_match():
    response = client.post(
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
    
# Successful password change
def test_successful_password_change():
    response = client.post(
        '/change-password',
        headers = {"Authorization": MOCK_TOKEN_TONI},
        json = {
            'current_password': 'FAMAFyC2022',
            'new_password': 'RightFormat1',
            'new_password_confirmation': 'RightFormat1'
        }
    )
    
    assert response.status_code == 200
    assert verify_password(
        'RightFormat1', 
        get_user_by_username('tonimondejar').hashed_password
    ) == True
    