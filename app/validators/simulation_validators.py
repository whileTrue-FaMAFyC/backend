from fastapi import HTTPException, status

from database.dao import robot_dao
from view_entities.simulation_view_entities import Simulation


def simulation_validator(creator_username: str, simulation_info: Simulation):
    valid_match = True
    detail = ""

    robots = 0

    if (simulation_info.num_rounds < 1 or simulation_info.num_rounds > 10000):
        code = status.HTTP_400_BAD_REQUEST
        valid_match = False
        detail += "Number of rounds has to be between 1 and 10000. "

    for r in simulation_info.robots:
        robots += 1
        robot = robot_dao.get_bot_by_owner_and_name(creator_username, r)
        if not robot:
            code = status.HTTP_409_CONFLICT
            valid_match = False
            detail += f"Robot {r} isn't in {creator_username}'s library. "

    if not robots in range(2, 5):
        code = status.HTTP_400_BAD_REQUEST
        valid_match = False
        detail += "The simulation needs between 2 and 4 robots. "

    if (not valid_match):
        raise HTTPException(
            status_code=code,
            detail=detail
        )

    return
