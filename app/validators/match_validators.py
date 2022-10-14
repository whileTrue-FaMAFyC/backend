from database.dao import match_dao, robot_dao
from fastapi import HTTPException
from view_entities.match_view_entities import NewMatchView

def new_match_val(new_match : NewMatchView):
    users_robot = robot_dao.belongs_to_user(new_match.creator_robot, 
                                         new_match.creator_user)
    name_in_use = match_dao.is_name_available(new_match.name, 
                                         new_match.creator_user)
    valid_match = True
    detail = ""

    if not(users_robot):
        valid_match = False
        detail += f"Robot {new_match.creator_robot} isn't "\
                  f"in {new_match.creator_user}'s library. "

    if name_in_use:
        valid_match = False
        detail += f"{new_match.creator_user} already has a match " \
                  f"named {new_match.name}. "
    
    if(new_match.min_players < 2 or new_match.min_players > 4):
        valid_match = False
        detail += "Minimum amount of players has to be between 2 and 4. "

    if(new_match.max_players < 2 or new_match.max_players > 4):
        valid_match = False
        detail += "Maximum amount of players has to be between 2 and 4. "

    if(new_match.min_players > new_match.max_players):
        valid_match = False
        detail += "Minimum amount of players can't be greater than " \
                  "maximum amount of players. "

    if(new_match.num_games < 1 or new_match.num_games > 200):
        valid_match = False
        detail += "Number of games has to be between 1 and 200. "

    if(new_match.num_rounds < 1 or new_match.num_rounds > 100000):
        valid_match = False
        detail += "Number of rounds has to be between 1 and 100000. "

    if(not valid_match):
        raise HTTPException(
            status_code = 400,
            detail = detail
        )
    
    return