from utils.match_utils import INTERNAL_ERROR_UPDATING_MATCH_INFO
from func_timeout import func_timeout

from database.dao.match_dao import get_match_info
from database.dao.match_results_dao import create_match_results
from services.game import Game
from utils.match_utils import match_winner
from utils.services_utils import create_robots_instances, INITIALIZATION_TIMEOUT

def execute_game_match(game: Game):
    for r in game.robots:
        try:
            func_timeout(timeout=INITIALIZATION_TIMEOUT, func=r.initialize)
        except:
            print('Robot timed out during initialization in match')
            r._increase_damage(100)

    while game.get_robots_alive() > 1 and game.get_rounds_remaining() > 0:
        game.execute_round()

    # Get survivors
    survivors = []
    for r in game.robots:
        if r.get_damage() < 100:
            survivors.append(r.get_robot_id())

    return survivors


def execute_match(match_id: int):
    match_info = get_match_info(match_id)
    robots_id = []
    games_results = {}

    for r in match_info.robots_joined:
        robots_id.append(r.robot_id)
        games_results[r.robot_id] = {"games_won": 0, "games_tied": 0}

    for i in range(match_info.num_games):
        robots = create_robots_instances(robots_id)
        game = Game(match_info.num_rounds, robots)
        survivors = execute_game_match(game)
        if len(survivors) > 1:
            for r in survivors:
                games_results[r]["games_tied"] += 1
        elif len(survivors) == 1:
            games_results[survivors[0]]["games_won"] += 1

    for i in robots_id:
        if not create_match_results(match_id, i, games_results[i]):
            raise INTERNAL_ERROR_UPDATING_MATCH_INFO

    return match_winner(robots_id, games_results)
