from fastapi.testclient import TestClient

from database.dao.match_dao import get_match_by_name_and_user
from main import app
from testing.helpers.generate_token import MOCK_TOKEN_BENJA
from utils.user_utils import INVALID_TOKEN_EXCEPTION
from utils.match_utils import *

client = TestClient(app)

def test_inexistent_match():
    response = client.delete("/matches/leave-match",
                          headers = {"Authorization": MOCK_TOKEN_BENJA},
                          json = {"match_id": 1024})

    assert response.status_code == INEXISTENT_MATCH_EXCEPTION.status_code
    assert response.json()["detail"] == INEXISTENT_MATCH_EXCEPTION.detail
    return

def test_user_not_joined():
    match_id = get_match_by_name_and_user('jmatch2', 'juliolcese').match_id

    response = client.delete("/matches/leave-match",
                          headers = {"Authorization": MOCK_TOKEN_BENJA},
                          json = {"match_id": match_id})

    assert response.status_code == USER_NOT_JOINED_EXCEPTION.status_code
    assert response.json()["detail"] == USER_NOT_JOINED_EXCEPTION.detail
    return

def test_invalid_token():
    match_id = get_match_by_name_and_user('match!', 'tonimondejar').match_id
    response = client.delete("/matches/leave-match",
                          headers = {"Authorization": "abc"},
                          json = {"match_id": match_id})
    
    assert response.status_code == INVALID_TOKEN_EXCEPTION.status_code
    assert response.json()["detail"] == INVALID_TOKEN_EXCEPTION.detail

def test_creator_cant_abandon():
    match_id = get_match_by_name_and_user('match1', 'bas_benja').match_id

    response = client.delete("/matches/leave-match",
                          headers = {"Authorization": MOCK_TOKEN_BENJA},
                          json = {"match_id": match_id})

    assert response.status_code == CREATOR_CANT_ABANDON_EXCEPTION.status_code
    assert response.json()["detail"] == CREATOR_CANT_ABANDON_EXCEPTION.detail
    return

# def test_successful_abandonment():
#     client.post(
#         "/matches/new-match",
#         headers = {'Authorization': MOCK_TOKEN_BENJA},
#         json = {
#             'name': 'myMatch',
#             'creator_robot': 'Bumblebee',
#             'min_players': 3,
#             'max_players': 4,
#             'num_games': 179,
#             'num_rounds': 5600,
#             'password': ''
#         }
#     )

#     match_id = get_match_by_name_and_user('myMatch', 'bas_benja').match_id
    
#     response = client.delete("/matches/abandon-match",
#                           headers = {"Authorization": MOCK_TOKEN_BENJA},
#                           json = {"match_id": match_id})

#     assert response.status_code == 200
#     return