from fastapi.testclient import TestClient

from main import app
from database.models.models import db, Robot
from testing.helpers.generate_token import MOCK_TOKEN_VALEN
from testing.helpers.mock_db import mock_bot_avatar
from utils.robot_utils import get_b64_from_path
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

expected_response =  [
    {"name": "R2D2", 
     "avatar": get_b64_from_path(mock_bot_avatar("valennegrelli", "R2D2"))}, 
    {"name": "WALL-E", "avatar": 'default'}, 
    {"name": "jarvis22", 
     "avatar": get_b64_from_path(mock_bot_avatar("valennegrelli", "jarvis22"))}
]

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