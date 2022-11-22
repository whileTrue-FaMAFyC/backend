from fastapi.testclient import TestClient

from main import app
from database.models.models import db, Robot
from testing.helpers.generate_token import MOCK_TOKEN_VALEN
from testing.helpers.mock_db import MOCK_AVATAR
from utils.user_utils import INVALID_TOKEN_EXCEPTION


client = TestClient(app)


# Test case where the user has no robots.
def test_no_robots():
    db.drop_table(Robot, with_all_data=True)
    db.create_tables()

    response = client.get(
        "/list-robots",
        headers={"Authorization": MOCK_TOKEN_VALEN}
    )

    assert response.status_code == 200
    assert response.json() == []
    return


def test_with_robots():
    response = client.get(
        "/list-robots",
        headers={"Authorization": MOCK_TOKEN_VALEN}
    )

    assert response.status_code == 200
    assert response.json() == [
        {"name": "R2D2", "avatar": MOCK_AVATAR, "stats": {"matches_played": 0, "matches_won": 0,
                                                          "matches_tied": 0, "matches_lost": 0, "games_win_rate": 0}},
        {"name": "WALL-E", "avatar": "", "stats": {"matches_played": 0, "matches_won": 0,
                                                   "matches_tied": 0, "matches_lost": 0, "games_win_rate": 0}},
        {"name": "jarvis22", "avatar": MOCK_AVATAR, "stats": {"matches_played": 0, "matches_won": 0,
                                                              "matches_tied": 0, "matches_lost": 0, "games_win_rate": 0}}
    ]


def test_invalid_token():
    response = client.get(
        "/list-robots",
        headers={"Authorization": ""}
    )

    assert response.status_code == INVALID_TOKEN_EXCEPTION.status_code
    assert response.json()["detail"] == INVALID_TOKEN_EXCEPTION.detail
