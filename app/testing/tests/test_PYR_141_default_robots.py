from random import randint
from fastapi.testclient import TestClient

from database.dao.robot_dao import *
from database.dao.user_dao import *
from main import app
from testing.helpers.generate_token import MOCK_TOKEN_SEBA
from utils.random_default_utils import *
from utils.robot_utils import *
from utils.shooter_default_utils import *

client = TestClient(app)


def test_default_robots_added():
    response = client.put(
        "/verifyuser/sebagiraudo",
        json={
            "verification_code": 123456
        }
    )

    assert response.status_code == 200

    assert get_bot_by_owner_and_name("sebagiraudo", "Shooter") is not None
    assert get_bot_by_owner_and_name("sebagiraudo", "Random") is not None

    response = client.post(
        "/new-simulation",
        headers={"authorization": MOCK_TOKEN_SEBA},
        json={
            "num_rounds": 100,
            "robots": ["Shooter", "Random"]
        }
    )

    assert response.status_code == 201
