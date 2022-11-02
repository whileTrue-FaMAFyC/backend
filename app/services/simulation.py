
from database.dao.robot_dao import get_bot_by_owner_and_name
from services.game import Game
from utils.services_utils import create_robots_instances
from view_entities.simulation_view_entities import Simulation

def execute_game_simulation(game: Game):
    frames = []
    for r in game.robots:
        r.initialize()
        frames.append({"robots": {}, "status": {}})
        frames[0]["robots"][r._id] = {"x": r.get_position()[0],
                                      "y": r.get_position()[1],
                                      "harmed": False,
                                      "died": False
                                    }

        frames[0]["status"][r._id] = 0
        frames[0]["missiles"] = {}

    while game.get_robots_alive() > 1 and game.get_rounds_remaining() > 0:
        game.execute_round()
        round = game._num_rounds_executed
        
        frames.append({"robots": {}, "status": {}, "missiles": {}})
      
        for r in game.robots:
            frames[round]["robots"][r._id] = {
                "x": r.get_position()[0],
                "y": r.get_position()[1],
                "harmed": frames[round-1]["status"][r._id] != r.get_damage(),
                "died": r.get_damage() >= 100
            }

            frames[round]["status"][r._id] = r.get_damage()

        for m in game._missiles:
            new = m.id in frames[round-1]["missiles"]
            frames[round]["missiles"][m.id] = {
                "x": m.current_position[0],
                "y": m.current_position[1],
                "exploded": m.current_position == m.final_position,
                "new": new
            }

    return frames

def execute_simulation(creator_username: str, simulation_info: Simulation):
    robots_id = []

    for r in simulation_info.robots:
        robot_in_db = get_bot_by_owner_and_name(creator_username, r)
        robots_id.append(robot_in_db.robot_id)

    robots = create_robots_instances(robots_id)
    game = Game(simulation_info.num_rounds, robots)
    frames = execute_game_simulation(game)

    return frames