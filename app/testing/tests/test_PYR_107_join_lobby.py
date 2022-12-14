from fastapi.testclient import TestClient

from database.dao.match_dao import get_match_by_name_and_user
from main import app
from testing.helpers.generate_token import MOCK_TOKEN_BENJA, MOCK_TOKEN_JULI, MOCK_TOKEN_TONI
from testing.helpers.match_helpers import create_possible_answer, expected_response_with_password
from testing.helpers.mock_db import MOCK_AVATAR

client = TestClient(app)


def test_join_lobby_creator():
    match_id = get_match_by_name_and_user('match1', 'bas_benja').match_id
    response = client.get(
        f'/matches/join-lobby?match_id={match_id}',
        headers={'Authorization': MOCK_TOKEN_BENJA},
    )

    assert response.status_code == 200
    assert response.json() in create_possible_answer([
        {
            "username": 'bas_benja',
            "user_avatar": MOCK_AVATAR,
            "robot_name": '0ptimusPrime',
            "robot_avatar": MOCK_AVATAR
        },
        {
            "username": 'juliolcese',
            "user_avatar": MOCK_AVATAR,
            "robot_name": 'astroGirl',
            "robot_avatar": MOCK_AVATAR
        }
    ])


def test_join_lobby_not_creator_joined():
    match_id = get_match_by_name_and_user('match1', 'bas_benja').match_id
    response = client.get(
        f'/matches/join-lobby?match_id={match_id}',
        headers={'Authorization': MOCK_TOKEN_JULI},
    )

    assert response.status_code == 200
    assert response.json() in create_possible_answer([
        {
            "username": 'bas_benja',
            "user_avatar": MOCK_AVATAR,
            "robot_name": '0ptimusPrime',
            "robot_avatar": MOCK_AVATAR
        },
        {
            "username": 'juliolcese',
            "user_avatar": MOCK_AVATAR,
            "robot_name": 'astroGirl',
            "robot_avatar": MOCK_AVATAR
        }
    ], "juliolcese", True, False)


def test_join_lobby_not_creator_not_joined():
    match_id = get_match_by_name_and_user('match1', 'bas_benja').match_id
    response = client.get(
        f'/matches/join-lobby?match_id={match_id}',
        headers={'Authorization': MOCK_TOKEN_TONI},
    )

    assert response.status_code == 200
    assert response.json() in create_possible_answer([
        {
            "username": 'bas_benja',
            "user_avatar": MOCK_AVATAR,
            "robot_name": '0ptimusPrime',
            "robot_avatar": MOCK_AVATAR
        },
        {
            "username": 'juliolcese',
            "user_avatar": MOCK_AVATAR,
            "robot_name": 'astroGirl',
            "robot_avatar": MOCK_AVATAR
        }
    ], "tonimondejar", False, False)


def test_join_lobby_with_results():
    match_id = get_match_by_name_and_user('match!', 'tonimondejar').match_id
    response = client.get(
        f'/matches/join-lobby?match_id={match_id}',
        headers={'Authorization': MOCK_TOKEN_JULI},
    )

    assert response.status_code == 200
    assert response.json()["results"] == [
        {"username": "tonimondejar", "robot_name": "_tron"}]


def test_join_lobby_with_password():
    match_id = get_match_by_name_and_user('match2', 'bas_benja').match_id
    response = client.get(
        f'/matches/join-lobby?match_id={match_id}',
        headers={'Authorization': MOCK_TOKEN_JULI},
    )

    assert response.status_code == 200
    assert response.json() == expected_response_with_password
