from fastapi.testclient import TestClient

from database.dao.match_dao import get_match_by_name_and_user, update_joining_user_match
from database.dao.robot_dao import get_bot_by_owner_and_name
from main import app
from testing.helpers.generate_token import MOCK_TOKEN_JULI, MOCK_TOKEN_BENJA
from testing.helpers.robot_stats_helpers import get_stats_by_robot

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
    
    
def test_one_winner():
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
        
    looser_robot_stats = get_stats_by_robot('bas_benja', 'RobotInutil')
    winner_robot_stats = get_stats_by_robot('juliolcese', 'RobotCrack')
    
    assert looser_robot_stats.matches_played == 1
    assert winner_robot_stats.matches_played == 1
    assert looser_robot_stats.matches_won == 0
    assert winner_robot_stats.matches_won == 1
    assert looser_robot_stats.matches_lost == 1
    assert winner_robot_stats.matches_lost == 0
    print(looser_robot_stats.games_win_rate)
    print(winner_robot_stats.games_win_rate)