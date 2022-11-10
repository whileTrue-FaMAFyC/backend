from fastapi.testclient import TestClient
import pytest

from controllers.match_controller import lobbys
from database.dao.match_dao import *
from main import app
from testing.helpers.generate_token import MOCK_TOKEN_BENJA, MOCK_TOKEN_JULI
from testing.helpers.match_helpers import user_and_robot_in_match
from testing.helpers.mock_db import mock_avatar, mock_bot_avatar
from utils.match_utils import *
from utils.robot_utils import get_b64_from_path
from utils.user_utils import INVALID_TOKEN_EXCEPTION

client = TestClient(app)

def test_inexistent_match():
    response = client.delete(f'/matches/leave-match/1024',
                          headers = {"Authorization": MOCK_TOKEN_BENJA})

    assert response.status_code == INEXISTENT_MATCH_EXCEPTION.status_code
    assert response.json()["detail"] == INEXISTENT_MATCH_EXCEPTION.detail
    return

def test_user_not_joined():
    match_id = get_match_by_name_and_user('jmatch2', 'juliolcese').match_id

    response = client.delete(f'/matches/leave-match/{match_id}',
                          headers = {"Authorization": MOCK_TOKEN_BENJA})

    assert response.status_code == USER_NOT_JOINED_EXCEPTION.status_code
    assert response.json()["detail"] == USER_NOT_JOINED_EXCEPTION.detail
    return

def test_invalid_token():
    match_id = get_match_by_name_and_user('match!', 'tonimondejar').match_id
    response = client.delete(f'/matches/leave-match/{match_id}',
                          headers = {"Authorization": "abc"})
    
    assert response.status_code == INVALID_TOKEN_EXCEPTION.status_code
    assert response.json()["detail"] == INVALID_TOKEN_EXCEPTION.detail

def test_creator_cant_abandon():
    match_id = get_match_by_name_and_user('match1', 'bas_benja').match_id

    response = client.delete(f'/matches/leave-match/{match_id}',
                          headers = {"Authorization": MOCK_TOKEN_BENJA})

    assert response.status_code == CREATOR_CANT_ABANDON_EXCEPTION.status_code
    assert response.json()["detail"] == CREATOR_CANT_ABANDON_EXCEPTION.detail
    return

@pytest.mark.asyncio
async def test_successful_leaving():
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

    update_joining_user_match("juliolcese", "astroGirl", match_id)

    assert user_and_robot_in_match(match_id, "juliolcese", "astroGirl")

    with client.websocket_connect(
            f"/matches/ws/follow-lobby/{match_id}?authorization={MOCK_TOKEN_BENJA}"
        ) as websocket:
            response = client.delete(
               f'matches/leave-match/{match_id}',
                headers={"Authorization": MOCK_TOKEN_JULI},
            )
            assert response.status_code == 200     

            data = websocket.receive_json()
            assert data == {
                "action": "leave",
                "data": {
                    "username": "juliolcese",
                    "user_avatar": get_b64_from_path(mock_avatar("juliolcese")),
                    "robot_name": "astroGirl",
                    "robot_avatar": get_b64_from_path(mock_bot_avatar("juliolcese", "astroGirl"))
                }
            }
            websocket.close()

    assert not user_and_robot_in_match(match_id, "juliolcese", "astroGirl")
    return