from fastapi.testclient import TestClient

from main import app
from database.models.models import db
from testing.helpers.generate_token import MOCK_TOKEN_BENJA
from utils.user_utils import INVALID_TOKEN_EXCEPTION


client = TestClient(app)


# Test case where there are no matches created
def test_no_matches():
    db.drop_all_tables(with_all_data=True)
    db.create_tables()

    response = client.get(
        "/matches/list-matches",
        headers={"Authorization": MOCK_TOKEN_BENJA}
    )

    assert response.status_code == 200
    assert response.json() == []


expected_response = [
    {"match_id": 1, "name": "match1", "creator_user": {"username": "bas_benja"},
     "max_players": 4, "robots_joined": 2},
    {"match_id": 2, "name": "match2", "creator_user": {"username": "bas_benja"},
        "max_players": 3, "robots_joined": 1},
    {"match_id": 3, "name": "match1", "creator_user": {"username": "juliolcese"},
        "max_players": 3, "robots_joined": 1},
    {"match_id": 4, "name": "jmatch2", "creator_user": {"username": "juliolcese"},
        "max_players": 3, "robots_joined": 1},
    {"match_id": 5, "name": "24601", "creator_user": {"username": "tonimondejar"},
        "max_players": 2, "robots_joined": 1},
    {"match_id": 6, "name": "match!", "creator_user": {"username": "tonimondejar"},
        "max_players": 4, "robots_joined": 3},
    {"match_id": 7, "name": "partidaza", "creator_user": {"username": "valennegrelli"},
        "max_players": 2, "robots_joined": 2}
]


# In this test we first create new matches and then analyze the behavior.
def test_with_matches():
    response = client.get(
        "/matches/list-matches",
        headers={"Authorization": MOCK_TOKEN_BENJA}
    )

    assert response.status_code == 200
    assert response.json() == expected_response


def test_invalid_token():
    response = client.get(
        "/matches/list-matches",
        headers={"Authorization": ""},
    )

    assert response.status_code == INVALID_TOKEN_EXCEPTION.status_code
    assert response.json()["detail"] == INVALID_TOKEN_EXCEPTION.detail


expected_response_owner = [
    {"match_id": 1, "name": "match1", "creator_user": {"username": "bas_benja"},
     "max_players": 4, "robots_joined": 2},
    {"match_id": 2, "name": "match2", "creator_user": {"username": "bas_benja"},
        "max_players": 3, "robots_joined": 1}
]


def test_owner_matches():
    response = client.get(
        "/matches/list-matches",
        headers={"Authorization": MOCK_TOKEN_BENJA},
        params={
            "is_owner": True
        }
    )

    assert response.status_code == 200
    assert response.json() == expected_response_owner


expected_response_not_joined = [
    {"match_id": 3, "name": "match1", "creator_user": {"username": "juliolcese"},
     "max_players": 3, "robots_joined": 1},
    {"match_id": 4, "name": "jmatch2", "creator_user": {"username": "juliolcese"},
        "max_players": 3, "robots_joined": 1},
    {"match_id": 5, "name": "24601", "creator_user": {"username": "tonimondejar"},
        "max_players": 2, "robots_joined": 1},
]


def test_not_joined_matches():
    response = client.get(
        "/matches/list-matches",
        headers={"Authorization": MOCK_TOKEN_BENJA},
        params={
            "is_joined": "False"
        }
    )

    assert response.status_code == 200
    assert response.json() == expected_response_not_joined


def test_started_matches():
    response = client.get(
        "/matches/list-matches",
        headers={"Authorization": MOCK_TOKEN_BENJA},
        params={
            "started": "True"
        }
    )

    assert response.status_code == 200
    assert response.json() == [
        {"match_id": 6, "name": "match!", "creator_user": {"username": "tonimondejar"},
        "max_players": 4, "robots_joined": 3}
    ]


def test_joined_not_owner_not_started():
    response = client.get(
        "/matches/list-matches",
        headers={"Authorization": MOCK_TOKEN_BENJA},
        params={
            "is_owner": "False",
            "is_joined": "True",
            "started": "False"
        }
    )

    assert response.status_code == 200
    assert response.json() == [
        {"match_id": 7, "name": "partidaza", "creator_user": {"username": "valennegrelli"},
        "max_players": 2, "robots_joined": 2}
    ]
