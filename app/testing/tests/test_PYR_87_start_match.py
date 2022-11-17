from fastapi.testclient import TestClient

from database.dao.match_dao import get_match_by_name_and_user, update_joining_user_match
from main import app
from testing.helpers.generate_token import MOCK_TOKEN_BENJA, MOCK_TOKEN_JULI, MOCK_TOKEN_TONI, MOCK_TOKEN_VALEN
from utils.match_utils import *

client = TestClient(app)

def new_match_post():
    response = client.post(
        "/matches/new-match",
        headers = {'Authorization': MOCK_TOKEN_JULI},
        json = {
            'name': "myMatch!",
            'creator_robot': 'RobotCrack',
            'min_players': 2,
            'max_players': 3,
            'num_games': 10,
            'num_rounds': 200,
            'password': ""
        }
    )
    assert response.status_code == 201


def test_inexistent_match():
    response = client.put(
        "/matches/start-match/1024",
        headers = {'authorization': MOCK_TOKEN_BENJA}
    )

    assert response.status_code == INEXISTENT_MATCH_EXCEPTION.status_code
    assert response.json()["detail"] == INEXISTENT_MATCH_EXCEPTION.detail


def test_not_creator():
    match_id = get_match_by_name_and_user("match1", "bas_benja").match_id
    response = client.put(
        f"/matches/start-match/{match_id}",
        headers = {'Authorization': MOCK_TOKEN_TONI}   
    )
    
    assert response.status_code == NOT_CREATOR.status_code
    assert response.json()["detail"] == NOT_CREATOR.detail


def test_already_started():
    match_id = get_match_by_name_and_user("match!", "tonimondejar").match_id
    response = client.put(
        f"/matches/start-match/{match_id}",
        headers = {'Authorization': MOCK_TOKEN_TONI}   
    )

    assert response.status_code == MATCH_ALREADY_STARTED.status_code
    assert response.json()["detail"] == MATCH_ALREADY_STARTED.detail


def test_not_enough_players():
    match_id = get_match_by_name_and_user("match1", "juliolcese").match_id
    response = client.put(
        f"/matches/start-match/{match_id}",
        headers = {'Authorization': MOCK_TOKEN_JULI}
    )
    
    assert response.status_code == NOT_ENOUGH_PLAYERS.status_code
    assert response.json()["detail"] == NOT_ENOUGH_PLAYERS.detail


def test_successful_start():
    new_match_post()

    match_id = get_match_by_name_and_user('myMatch!', 'juliolcese').match_id

    update_joining_user_match("bas_benja", "RobotInutil", match_id)
    
    with client.websocket_connect(
        f"/matches/ws/follow-lobby/{match_id}?authorization={MOCK_TOKEN_BENJA}"
    ) as websocket:
        response = client.put(
            f'matches/start-match/{match_id}',
            headers={"Authorization": MOCK_TOKEN_JULI},
        )
        
        assert response.status_code == 200

        data = websocket.receive_json()
        assert data == {
            "action": "start",
            "data": ""
        }
        
        data = websocket.receive_json()
        assert data == {
            "action": "results",
            "data": {
                "winners": [{
                    "username": "juliolcese",
                    "robot_name": "RobotCrack"
                }]
            }
        }
        websocket.close()

    match = get_match_by_name_and_user('myMatch!', 'juliolcese')
    assert match.started