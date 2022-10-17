from fastapi import HTTPException, status

from database.dao import match_dao, robot_dao
from view_entities.match_view_entities import NewMatch

def new_match_validator(creator_username: str, new_match : NewMatch):
    # To check if the user has a robot with the provided name
    users_robot = robot_dao.get_bot_by_owner_and_name(creator_username, 
                                                      new_match.creator_robot)
    # To check if the user already created a match with the provided name
    name_in_use = match_dao.get_match_by_name_and_user(new_match.name, 
                                                       creator_username)
    valid_match = True
    detail = ""

    if not(users_robot):
        valid_match = False
        detail += f"Robot {new_match.creator_robot} isn't "\
                  f"in {creator_username}'s library. "

    if name_in_use:
        valid_match = False
        detail += f"{creator_username} already has a match " \
                  f"named {new_match.name}. "
    
    if (new_match.min_players < 2 or new_match.min_players > 4):
        valid_match = False
        detail += "Minimum amount of players has to be between 2 and 4. "

    if (new_match.max_players < 2 or new_match.max_players > 4):
        valid_match = False
        detail += "Maximum amount of players has to be between 2 and 4. "

    if (new_match.min_players > new_match.max_players):
        valid_match = False
        detail += "Minimum amount of players can't be greater than " \
                  "maximum amount of players. "

    if (new_match.num_games < 1 or new_match.num_games > 200):
        valid_match = False
        detail += "Number of games has to be between 1 and 200. "

    if (new_match.num_rounds < 1 or new_match.num_rounds > 10000):
        valid_match = False
        detail += "Number of rounds has to be between 1 and 10000. "

    if (not valid_match):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )
    
    return