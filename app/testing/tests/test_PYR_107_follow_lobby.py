from fastapi.testclient import TestClient

from controllers.match_controller import lobbys
from main import app
from testing.helpers.generate_token import MOCK_TOKEN_BENJA, MOCK_TOKEN_JULI, MOCK_TOKEN_TONI, MOCK_TOKEN_VALEN
from database.dao.match_dao import get_match_by_name_and_user

tokens = [MOCK_TOKEN_BENJA, MOCK_TOKEN_JULI, MOCK_TOKEN_TONI, MOCK_TOKEN_VALEN]


client = TestClient(app)


# Several users join the same lobby
def test_websockets_for_same_lobby():
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
    
    
    match_id = get_match_by_name_and_user('myMatch', 'bas_benja').match_id

    assert len(lobbys[match_id].active_connections) == 0
    
    for token in tokens:
        with client.websocket_connect(
            f"/matches/ws/follow-lobby/{match_id}?token={token}"
        ) as websocket:
            websocket.close()
    
    assert len(lobbys[match_id].active_connections) == 4
