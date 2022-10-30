from fastapi.testclient import TestClient
from testing.helpers.generate_token import MOCK_TOKEN_VALEN, MOCK_TOKEN_JULI
from testing.helpers.mock_db import MOCK_SOURCE_CODE, MOCK_AVATAR

from main import app


client = TestClient(app)


# Try creating a bot that already exists in the database
def test_create_existent_bot():
    response = client.post(
        '/create-bot',
        headers={'Authorization': MOCK_TOKEN_VALEN},
        json = {
            'name': 'jarvis22',
            'source_code': MOCK_SOURCE_CODE,
            'bot_filename': 'mybot.py',
            'avatar': MOCK_AVATAR
        }
    )
    
    assert response.status_code == 409
    assert response.json() == {
        'detail': "User already has a bot with this name."
    }


# Invalid token
def test_invalid_token():
    response = client.post(
        '/create-bot',
        headers={'Authorization': 'dsafaerafasf.sfaserfasf'},
        json = {
            'name': 'jarvis22',
            'source_code': MOCK_SOURCE_CODE,
            'bot_filename': 'mybot.py',
            'avatar': MOCK_AVATAR
        }
    )
    
    assert response.status_code == 401
    assert response.json() == {
        'detail': "Invalid token. Not authorized."
    }


# Create new bot succesfully
def test_create_bot():
    response = client.post(
        '/create-bot',
        headers={'Authorization': MOCK_TOKEN_JULI},
        json = {            
            'name': 'R2D2',
            'source_code': MOCK_SOURCE_CODE,
            'bot_filename': 'mybot.py',
            'avatar': MOCK_AVATAR
        }
    )
    
    assert response.status_code == 200
    assert response.json() == True
