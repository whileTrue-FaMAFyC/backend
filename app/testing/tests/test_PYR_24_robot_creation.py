from fastapi.testclient import TestClient
from pony.orm import db_session

from app.database.dao.robot_dao import get_robot_by_owner_and_name
from testing.helpers.generate_token import MOCK_TOKEN_VALEN, MOCK_TOKEN_JULI
from testing.helpers.mock_db import MOCK_SOURCE_CODE, MOCK_AVATAR

from main import app


client = TestClient(app)


# Try creating a robot that already exists in the database
def test_create_existent_robot():
    response = client.post(
        '/create-robot',
        headers={'Authorization': MOCK_TOKEN_VALEN},
        json={
            'name': 'jarvis22',
            'source_code': MOCK_SOURCE_CODE,
            'bot_filename': 'myrobot.py',
            'avatar': MOCK_AVATAR
        }
    )

    assert response.status_code == 409
    assert response.json() == {
        'detail': "User already has a robot with this name."
    }


# Invalid token
def test_invalid_token():
    response = client.post(
        '/create-robot',
        headers={'Authorization': 'dsafaerafasf.sfaserfasf'},
        json={
            'name': 'jarvis22',
            'source_code': MOCK_SOURCE_CODE,
            'bot_filename': 'myrobot.py',
            'avatar': MOCK_AVATAR
        }
    )

    assert response.status_code == 401
    assert response.json() == {
        'detail': "Invalid token. Not authorized."
    }


# Create new robot succesfully
def test_create_robot():
    response = client.post(
        '/create-robot',
        headers={'Authorization': MOCK_TOKEN_JULI},
        json={
            'name': 'R2D2',
            'source_code': MOCK_SOURCE_CODE,
            'bot_filename': 'myrobot.py',
            'avatar': MOCK_AVATAR
        }
    )

    with db_session:
        new_robot = get_robot_by_owner_and_name('juliolcese', 'R2D2')
        assert new_robot is not None
        assert new_robot.stats is not None

    assert response.status_code == 201
    assert response.json() == True
