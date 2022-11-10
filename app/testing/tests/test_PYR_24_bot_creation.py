import os

from fastapi.testclient import TestClient
from testing.helpers.generate_token import MOCK_TOKEN_VALEN, MOCK_TOKEN_JULI, MOCK_TOKEN_BENJA
from utils.user_utils import USERS_ASSETS
from main import app

client = TestClient(app)

def mock_source_code():
    return ('cool_robot.py', open('./testing/helpers/cool_robot.py'), 'application/x-python-code')

def mock_avatar():
    return ('avatar2.png', open('./testing/helpers/avatar2.png', 'rb'), 'image/png' )



# Try creating a bot that already exists in the database
def test_create_existent_bot():
    response = client.post(
        '/create-bot',
        headers={'Authorization': MOCK_TOKEN_VALEN},
        data={
            'bot_name': 'jarvis22',
        },
        files={
            'bot_source_code': mock_source_code(),
            'bot_avatar': mock_avatar()
        }       
    )
    
    assert response.status_code == 409
    assert response.json() == {
        'detail': "User already has a bot with this name."
    }



# # Invalid token
def test_invalid_token():
    response = client.post(
        '/create-bot',
        headers={'Authorization': 'dsafaerafasf.sfaserfasf'},
        data={
            'bot_name': 'jarvis22',
        },
        files={
            'bot_source_code': mock_source_code(),
            'bot_avatar': mock_avatar()
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
        data={
            'bot_name': 'R2D2',
        },
        files={
            'bot_source_code':mock_source_code(),
            'bot_avatar': mock_avatar()
        }
    )
    
    assert response.status_code == 200
    assert os.path.exists(f'{USERS_ASSETS}/juliolcese/avatar_cool_robot.png') == True
    assert os.path.exists(f'{USERS_ASSETS}/juliolcese/cool_robot.py')
    os.remove(f'{USERS_ASSETS}/juliolcese/avatar_cool_robot.png')
    os.remove(f'{USERS_ASSETS}/juliolcese/cool_robot.py')
    os.rmdir(f'{USERS_ASSETS}/juliolcese/')
