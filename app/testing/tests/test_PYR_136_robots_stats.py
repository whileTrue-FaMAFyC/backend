from fastapi.testclient import TestClient

from database.dao.match_dao import get_match_by_name_and_user, update_joining_user_match
from main import app
from testing.helpers.generate_token import MOCK_TOKEN_JULI, MOCK_TOKEN_BENJA, MOCK_TOKEN_LUCAS
from testing.helpers.robot_stats_helpers import get_stats_by_robot

client = TestClient(app)


def new_match_post_juli(match_name: str):
    response = client.post(
        "/matches/new-match",
        headers={'Authorization': MOCK_TOKEN_JULI},
        json={
            'name': match_name,
            'creator_robot': 'RobotCrack',
            'min_players': 2,
            'max_players': 3,
            'num_games': 10,
            'num_rounds': 200,
            'password': ""
        }
    )
    assert response.status_code == 201


def new_match_post_benja(match_name: str):
    response = client.post(
        "/matches/new-match",
        headers={'Authorization': MOCK_TOKEN_BENJA},
        json={
            'name': match_name,
            'creator_robot': 'RobotInutil',
            'min_players': 2,
            'max_players': 3,
            'num_games': 10,
            'num_rounds': 200,
            'password': ""
        }
    )
    assert response.status_code == 201


def test_all_stats():
    new_match_post_juli("myMatch!")

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
    assert looser_robot_stats.matches_tied == 0
    assert winner_robot_stats.matches_tied == 0
    assert looser_robot_stats.games_win_rate >= 0
    assert winner_robot_stats.games_win_rate > 0

    # Now, play another match with RobotCrack and another one with RobotInutil
    # to check that their stats are updating
    new_match_post_benja("tiedMatch")

    match_id = get_match_by_name_and_user('tiedMatch', 'bas_benja').match_id
    update_joining_user_match("lucasca22ina", "RobotInutil", match_id)

    with client.websocket_connect(
        f"/matches/ws/follow-lobby/{match_id}?authorization={MOCK_TOKEN_LUCAS}"
    ) as websocket:
        response = client.put(
            f'matches/start-match/{match_id}',
            headers={"Authorization": MOCK_TOKEN_BENJA},
        )

        assert response.status_code == 200

        data = websocket.receive_json()
        assert data == {
            "action": "start",
            "data": ""
        }

        data = websocket.receive_json()
        assert (
            data == {
                "action": "results",
                "data": {
                    "winners": [
                        {
                            "username": "lucasca22ina",
                            "robot_name": "RobotInutil"
                        },
                        {
                            "username": "bas_benja",
                            "robot_name": "RobotInutil"
                        }
                    ]
                }
            }
            or data == {
                "action": "results",
                "data": {
                    "winners": [
                        {
                            "username": "bas_benja",
                            "robot_name": "RobotInutil"
                        },
                        {
                            "username": "lucasca22ina",
                            "robot_name": "RobotInutil"
                        }
                    ]
                }
            }
        )

        websocket.close()

    tied_robot_stats_benja = get_stats_by_robot('bas_benja', 'RobotInutil')
    tied_robot_stats_lucas = get_stats_by_robot('lucasca22ina', 'RobotInutil')

    assert tied_robot_stats_benja.matches_played == 2
    assert tied_robot_stats_lucas.matches_played == 1
    assert tied_robot_stats_benja.matches_won == 0
    assert tied_robot_stats_lucas.matches_won == 0
    assert tied_robot_stats_benja.matches_lost == 1
    assert tied_robot_stats_lucas.matches_lost == 0
    assert tied_robot_stats_benja.matches_tied == 1
    assert tied_robot_stats_lucas.matches_tied == 1
    assert tied_robot_stats_benja.games_win_rate >= 0
    assert tied_robot_stats_lucas.games_win_rate >= 0
