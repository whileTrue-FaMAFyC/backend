
from database.dao.robot_dao import get_bot_by_owner_and_name, get_bot_by_id
from services.game import Game
from utils.services_utils import create_robots_instances, OUT_OF_BOUNDS
from view_entities.robot_view_entities import RobotInSimulation
from view_entities.simulation_view_entities import Simulation

def execute_game_simulation(game: Game):
    frames = []
    robots = []
    frames.append({"robots": {}})
    for r in game.robots:
        r.initialize()
        frames[0]["robots"][r._id_in_game] = {"x": r.get_position()[0],
                                              "y": r.get_position()[1],
                                              "harmed": False,
                                              "died": False, 
                                              "status": 0
                                             }
        frames[0]["missiles"] = {}
        name = get_bot_by_id(r._id).name
        robots.append(RobotInSimulation(name=name, id=r._id_in_game))

    while game.get_robots_alive() > 1 and game.get_rounds_remaining() > 0:
        game.execute_round()
        round = game._num_rounds_executed
        frames.append({"robots": {}, "missiles": {}})
      
        for r in game.robots:
            position = r.get_position() if r.get_position() != OUT_OF_BOUNDS else r._final_position
            frames[round]["robots"][r._id_in_game] = {
                "x": position[0],
                "y": position[1],
                "harmed": frames[round-1]["robots"][r._id_in_game]["status"] != r.get_damage(),
                "died": r.get_damage() >= 100,
                "status": r.get_damage()
            }

        for m in game._missiles:
            new = m.id in frames[round-1]["missiles"]
            frames[round]["missiles"][m.id] = {
                "initial_x": m.initial_position[0],
                "initial_y": m.initial_position[1],
                "x": m.current_position[0],
                "y": m.current_position[1],
                "exploded": m.current_position == m.final_position,
                "new": new
            }

    return frames, robots

def execute_simulation(creator_username: str, simulation_info: Simulation):
    robots_id = []

    for r in simulation_info.robots:
        robot_in_db = get_bot_by_owner_and_name(creator_username, r)
        robots_id.append(robot_in_db.robot_id)

    robots = create_robots_instances(robots_id)
    game = Game(simulation_info.num_rounds, robots)
    frames, robots = execute_game_simulation(game)

    return frames, robots