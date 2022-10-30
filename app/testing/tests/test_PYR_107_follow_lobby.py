from fastapi.testclient import TestClient
import pytest

from main import app
from testing.helpers.generate_token import MOCK_TOKEN_BENJA
from database.dao.match_dao import *


client = TestClient(app)

def test_websocket():
    client.post(
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

    match_id = get_match_by_name_and_user('myMatch', 'bas_benja').match_id
    
    with client.websocket_connect(
        f"/matches/ws/follow-lobby/{match_id}?token={MOCK_TOKEN_BENJA}"
    ) as websocket:
        websocket.send_text("Hello there")
        data = websocket.receive_text()
        assert data == "Hello there"
        websocket.close()
