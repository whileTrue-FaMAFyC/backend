from fastapi.testclient import TestClient

from database.dao.match_dao import get_match_by_name_and_user
from main import app
from testing.helpers.generate_token import MOCK_TOKEN_BENJA, MOCK_TOKEN_JULI, MOCK_TOKEN_TONI
from testing.helpers.mock_db import MOCK_AVATAR

client = TestClient(app)


def test_join_lobby_creator():    
    match_id = get_match_by_name_and_user('match1', 'bas_benja').match_id    
    response = client.get(
        f'/matches/join-lobby?match_id={match_id}',
        headers = {'Authorization': MOCK_TOKEN_BENJA},
    )    
    
    assert response.status_code == 200
    assert response.json() == {
        'requester_username': 'bas_benja',
        'name': 'match1',
        'creator_username': 'bas_benja',
        'min_players': 2,
        'max_players': 4,
        'num_games': 10,
        'num_rounds': 1570,
        'users_joined': 2,
        'user_robot': {
            'bas_benja': [MOCK_AVATAR, '0ptimusPrime', MOCK_AVATAR], 
            'juliolcese': [MOCK_AVATAR, 'astroGirl', MOCK_AVATAR]
        },
        'started': False,
        'im_in': True,
        'is_creator': True
    }


def test_join_lobby_not_creator_joined():
    match_id = get_match_by_name_and_user('match!', 'tonimondejar').match_id    
    response = client.get(
        f'/matches/join-lobby?match_id={match_id}',
        headers = {'Authorization': MOCK_TOKEN_JULI},
    )    
    
    assert response.status_code == 200
    assert response.json() == {
        'requester_username': 'juliolcese',
        'name': 'match!',
        'creator_username': 'tonimondejar',
        'min_players': 4,
        'max_players': 4,
        'num_games': 200,
        'num_rounds': 1,
        'users_joined': 3,
        'user_robot': {
            'tonimondejar': ['', '_tron', MOCK_AVATAR],
            'bas_benja': [MOCK_AVATAR, 'Bumblebee', MOCK_AVATAR], 
            'juliolcese': [MOCK_AVATAR, 'automatax', MOCK_AVATAR]
        },
        'started': False,
        'im_in': True,
        'is_creator': False
    }

 
def test_join_lobby_not_creator_not_joined():
    match_id = get_match_by_name_and_user('match1', 'bas_benja').match_id    
    response = client.get(
        f'/matches/join-lobby?match_id={match_id}',
        headers = {'Authorization': MOCK_TOKEN_TONI},
    )    
    
    assert response.status_code == 200
    assert response.json() == {
        'requester_username': 'tonimondejar',
        'name': 'match1',
        'creator_username': 'bas_benja',
        'min_players': 2,
        'max_players': 4,
        'num_games': 10,
        'num_rounds': 1570,
        'users_joined': 2,
        'user_robot': {
            'bas_benja': [MOCK_AVATAR, '0ptimusPrime', MOCK_AVATAR], 
            'juliolcese': [MOCK_AVATAR, 'astroGirl', MOCK_AVATAR]
        },       
        'started': False,
        'im_in': False,
        'is_creator': False
    }