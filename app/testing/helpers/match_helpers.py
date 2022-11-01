from itertools import permutations


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
        'results':[]
    })
    
    return possible_answers
