from itertools import permutations
from pony.orm import db_session

from database.models.models import Match
from testing.helpers.mock_db import mock_avatar, mock_bot_avatar

def create_possible_answer(possible_users, requester_username="bas_benja", im_in=True, is_creator=True):
    possible_answers = []
    users_order = permutations(possible_users)
    for user in users_order:
        possible_answers.append({
        'requester_username': requester_username,
        'name': 'match1',
        'creator_username': 'bas_benja',
        'min_players': 2,
        'max_players': 4,
        'num_games': 10,
        'num_rounds': 1570,
        'users_joined': 2,
        'user_robot': list(user),
        'started': False,
        'im_in': im_in,
        'is_creator': is_creator,
        'results':[],
        'has_password': False
    })
    
    return possible_answers


@db_session
def user_and_robot_in_match(match_id: int, joining_user:str, joining_robot: str):
    match_in_db = Match.get(match_id=match_id)
    is_in_match = False
    for r in match_in_db.robots_joined:
        if r.name == joining_robot and r.owner.username == joining_user:
            is_in_match = True
    return is_in_match


expected_response_with_password = {
        'requester_username': 'juliolcese',
        'name': 'match2',
        'creator_username': 'bas_benja',
        'min_players': 3,
        'max_players': 3,
        'num_games': 200,
        'num_rounds': 100000,
        'users_joined': 1,
        'user_robot': [{
                "username":'bas_benja',
                "user_avatar": mock_avatar('bas_benja'),
                "robot_name": 'Bumblebee',
                "robot_avatar": mock_bot_avatar('bas_benja', 'dumb_robot.py')
            }],
        'started': False,
        'im_in': False,
        'is_creator': False,
        'results':[],
        'has_password': True
    }