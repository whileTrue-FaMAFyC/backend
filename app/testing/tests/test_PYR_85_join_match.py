from fastapi.testclient import TestClient
import pytest

from controllers.match_controller import lobbys
from database.dao.match_dao import get_match_by_name_and_user
from main import app
from testing.helpers.generate_token import *
from testing.helpers.match_helpers import user_and_robot_in_match
from testing.helpers.mock_db import MOCK_AVATAR
from utils.match_utils import *

client = TestClient(app)

def test_inexistent_robot():
    match_id = get_match_by_name_and_user('match1', 'bas_benja').match_id    
    response = client.post(
        f'/matches/join-match/{match_id}',
        headers = {'Authorization': MOCK_TOKEN_BENJA},
        json={
            "joining_robot": "_tron"
        }
    )

    assert response.status_code == INEXISTENT_ROBOT.status_code
    assert response.json()["detail"] == INEXISTENT_ROBOT.detail

def test_inexistent_match():
    response = client.post(
        f'/matches/join-match/1024',
        headers = {'Authorization': MOCK_TOKEN_BENJA},
        json={
            "match_password": "",
            "joining_robot": "Bumblebee"
        }
    )
    
    assert response.status_code == INEXISTENT_MATCH_EXCEPTION.status_code
    assert response.json()["detail"] == INEXISTENT_MATCH_EXCEPTION.detail

def test_user_already_joined():
    match_id = get_match_by_name_and_user('match1', 'bas_benja').match_id    
    response = client.post(
        f'/matches/join-match/{match_id}',
        headers = {'Authorization': MOCK_TOKEN_BENJA},
        json={
            "joining_robot": "0ptimusPrime"
        }
    )

    assert response.status_code == USER_ALREADY_JOINED.status_code
    assert response.json()["detail"] == USER_ALREADY_JOINED.detail


def test_incorrect_password():
    match_id = get_match_by_name_and_user('match1', 'juliolcese').match_id
    response = client.post(
        f'/matches/join-match/{match_id}',
        headers = {'Authorization': MOCK_TOKEN_BENJA},
        json={
            "match_password": "Incorrect!",
            "joining_robot": "0ptimusPrime"
        }
    )
    
    assert response.status_code == INCORRECT_PASSWORD.status_code
    assert response.json()["detail"] == INCORRECT_PASSWORD.detail

def test_no_password():
    match_id = get_match_by_name_and_user('match1', 'juliolcese').match_id
    response = client.post(
        f'/matches/join-match/{match_id}',
        headers = {'Authorization': MOCK_TOKEN_BENJA},
        json={
            "match_password": "",
            "joining_robot": "0ptimusPrime"
        }
    )
    
    assert response.status_code == INCORRECT_PASSWORD.status_code
    assert response.json()["detail"] == INCORRECT_PASSWORD.detail

def test_max_players_reached():
    match_id = get_match_by_name_and_user('partidaza', 'valennegrelli').match_id
    response = client.post(
        f'/matches/join-match/{match_id}',
        headers = {'Authorization': MOCK_TOKEN_TONI},
        json={
            "match_password": "",
            "joining_robot": "_tron"
        }
    )
    
    assert response.status_code == MAX_PLAYERS_REACHED.status_code
    assert response.json()["detail"] == MAX_PLAYERS_REACHED.detail    


def test_match_already_started():
    match_id = get_match_by_name_and_user('match!', 'tonimondejar').match_id
    response = client.post(
        f'/matches/join-match/{match_id}',
        headers = {'Authorization': MOCK_TOKEN_VALEN},
        json={
            "match_password": "pw",
            "joining_robot": "R2D2"
        }
    )
    
    assert response.status_code == MATCH_ALREADY_STARTED.status_code
    assert response.json()["detail"] == MATCH_ALREADY_STARTED.detail


@pytest.mark.asyncio
async def test_successful_join_match():
    response = client.post(
        "/matches/new-match",
        headers = {'Authorization': MOCK_TOKEN_BENJA},
        json = {
            'name': 'myMatch',
            'creator_robot': 'Bumblebee',
            'min_players': 3,
            'max_players': 4,
            'num_games': 179,
            'num_rounds': 5600,
            'password': ''
        }
    )

    assert response.status_code == 201
    assert len(lobbys) > 0

    match_id = get_match_by_name_and_user('myMatch', 'bas_benja').match_id
    with client.websocket_connect(
            f"/matches/ws/follow-lobby/{match_id}?authorization={MOCK_TOKEN_JULI}"
        ) as websocket:
            assert not user_and_robot_in_match(match_id, "tonimondejar", "_tron")

            response = client.post(
                f"/matches/join-match/{match_id}",
                headers={"Authorization": MOCK_TOKEN_TONI},
                json={
                    "joining_robot": "_tron"
                }
            )

            assert response.status_code == 200
            assert user_and_robot_in_match(match_id, "tonimondejar", "_tron")

            data = websocket.receive_json()
            assert data == {
                "action": "join",
                "data": {
                    "username": "tonimondejar",
                    "user_avatar": "",
                    "robot_name": "_tron",
                    "robot_avatar": MOCK_AVATAR
                }
            }
            websocket.close()
