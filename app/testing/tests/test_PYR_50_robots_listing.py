from fastapi.testclient import TestClient

from main import app
from database.models.models import db, Robot
from testing.helpers.generate_token import MOCK_TOKEN_VALEN
from testing.helpers.mock_db import mock_bot_avatar
from utils.user_utils import INVALID_TOKEN_EXCEPTION


client = TestClient(app)


# Test case where the user has no robots.
def test_no_robots():
    db.drop_table(Robot, with_all_data=True)
    db.create_tables()

    response = client.get(
        "/list-robots",
        headers = {"Authorization": MOCK_TOKEN_VALEN}
    )
    
    assert response.status_code == 200
    assert response.json() == []
    return

expected_response =  [{"name": "R2D2", "avatar": mock_bot_avatar("valennegrelli", "dumb_robot.py")}, 
                      {"name": "WALL-E", "avatar": 'default'}, 
                      {"name": "jarvis22", "avatar": mock_bot_avatar("valennegrelli", "running_robot.py")}]

def test_with_robots():
    response = client.get(
        "/list-robots",
        headers = {"Authorization": MOCK_TOKEN_VALEN}
    )

    assert response.status_code == 200
    assert response.json() == expected_response

def test_invalid_token():
    response = client.get(
        "/list-robots",
        headers = {"Authorization": ""}
    )

    assert response.status_code == INVALID_TOKEN_EXCEPTION.status_code
    assert response.json()["detail"] == INVALID_TOKEN_EXCEPTION.detail