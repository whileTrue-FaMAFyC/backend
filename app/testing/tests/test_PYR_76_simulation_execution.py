from fastapi.testclient import TestClient

from main import app
from database.dao.robot_dao import get_bot_by_owner_and_name
from testing.helpers.generate_token import MOCK_TOKEN_BENJA

client = TestClient(app)

def test_invalid_rounds():
    response = client.post(
        "/new-simulation",
        headers = {"authorization": MOCK_TOKEN_BENJA},
        json = {
            "num_rounds": 1000000,
            "robots": ["Bumblebee", "0ptimusPrime"]
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Number of rounds has to be between 1 and 10000. "


def test_not_creators_robot():
    response = client.post(
        "/new-simulation",
        headers = {"authorization": MOCK_TOKEN_BENJA},
        json = {
            "num_rounds": 100,
            "robots": ["Bumblebee", "0ptimusPrime", "invalid"]
        }
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Robot invalid isn't in bas_benja's library. "

def test_invalid_robot_amount():
    response = client.post(
        "/new-simulation",
        headers = {"authorization": MOCK_TOKEN_BENJA},
        json = {
            "num_rounds": 100,
            "robots": ["Bumblebee"]
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "The simulation needs between 2 and 4 robots. "

def test_successful_creation():
    response = client.post(
        "/new-simulation",
        headers = {"authorization": MOCK_TOKEN_BENJA},
        json = {
            "num_rounds": 100,
            "robots": ["Bumblebee", "0ptimusPrime"]
        }
    )

    assert response.status_code == 201
    assert response.json()["names"] == [{"name": "Bumblebee",
                                         "id": 0},
                                        {"name": "0ptimusPrime",
                                         "id": 1}
    ]


def test_repeated_robot():
    response = client.post(
        "/new-simulation",
        headers = {"authorization": MOCK_TOKEN_BENJA},
        json = {
            "num_rounds": 100,
            "robots": ["Bumblebee", "Bumblebee"]
        }
    )

    assert response.status_code == 201
    assert response.json()["names"] == [{"name": "Bumblebee",
                                         "id": 0},
                                        {"name": "Bumblebee",
                                         "id": 1}
    ]
