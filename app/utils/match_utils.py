from fastapi import HTTPException, status
from pony.orm import db_session
from typing import Dict, List

from database.models.models import Match 
from database.dao.robot_dao import get_name_and_creator_by_id
from view_entities.match_view_entities import *
from view_entities.robot_view_entities import *


ERROR_CREATING_MATCH = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal error creating the match. "
)

INEXISTENT_ROBOT = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Robot selected is not in the user's library."
)

USER_ALREADY_JOINED = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The user has already joined."
)

INCORRECT_PASSWORD = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect password."
)

MAX_PLAYERS_REACHED = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Max players reached. Cannot join the match."
)

MATCH_ALREADY_STARTED = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The match has already started."
)

INTERNAL_ERROR_UPDATING_MATCH_INFO = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal error when updating the match info."
)

INEXISTENT_MATCH_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The match doesn't exist."
)

ERROR_DELETING_USER = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal error removing the user from the match."
)

USER_NOT_JOINED_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The user isn't in the match."
)

CREATOR_CANT_ABANDON_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The creator can't abandon the match."
)

# Transforms the matches selected from the database to the format that will be
# sent to the frontend.
@db_session
def match_db_to_view(matches: Match): # No es list[Match] o algo así?
    matches_info = [MatchInfo.from_orm(m) for m in matches]
    all_robots_joined = []
    info_and_robots = []

    for m in matches:
       all_robots_joined.append(len(m.robots_joined))

    for i in range(0, len(matches_info)):
        info_and_robots.append(
            ShowMatch(
                match_id=matches_info[i].match_id,
                name=matches_info[i].name,
                creator_user=matches_info[i].creator_user,
                max_players=matches_info[i].max_players,
                robots_joined=all_robots_joined[i]
            )
        )

    return info_and_robots


def match_winner(robots_id: List[int], game_results: Dict[int, Dict[str, int]]):
    max_won = 0
    max_tied = 0
    winners_robots = []
    tied_robots = []
    winners = []

    for i in robots_id:
        if game_results[i]["games_won"] == max_won:
            winners_robots.append(i)
        elif game_results[i]["games_won"] > max_won:
            max_won = game_results[i]["games_won"]
            winners_robots = [i]
    
    if len(winners_robots) > 1:
        for i in winners_robots:
            if game_results[i]["games_tied"] == max_tied:
                tied_robots.append(i)
            elif game_results[i]["games_tied"] > max_tied:
                max_tied = game_results[i]["games_tied"]
                tied_robots = [i]
        winners_robots = tied_robots
    
    for r in winners_robots:
        winners.append(get_name_and_creator_by_id(r))
        
    return winners