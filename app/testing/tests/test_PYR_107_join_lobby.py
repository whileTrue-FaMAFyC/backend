from fastapi.testclient import TestClient

from database.dao.match_dao import get_match_by_name_and_user
from main import app
from testing.helpers.generate_token import MOCK_TOKEN_BENJA


client = TestClient(app)


def test_join_lobby():    
    match_id = get_match_by_name_and_user('match1', 'bas_benja').match_id    
    
    response = client.get(
        f'/matches/join-lobby/?match_id={match_id}',
        headers = {'Authorization': MOCK_TOKEN_BENJA},
    )    
    
    assert response.status_code == 200
    assert response.json() == {
        'name': 'match1',
        'creator_username': 'bas_benja',
        'min_players': 2,
        'max_players': 4,
        'num_games': 10,
        'num_rounds': 1570,
        'users_joined': 2,
        'user_robot': {'bas_benja': '0ptimusPrime', 'juliolcese': 'astroGirl'},
        'started': False
    }
