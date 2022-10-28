from fastapi import HTTPException, status
from pony.orm import db_session

from database.models.models import Match 
from view_entities.match_view_entities import *
from view_entities.robot_view_entities import *


ERROR_CREATING_MATCH = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal error creating the match. "
)

NOT_EXISTENT_ROBOT = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Robot selected is not in your library."
)

NOT_EXISTENT_MATCH = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The match selected does not exists."
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

# Transforms the matches selected from the database to the format that will be
# sent to the frontend.
@db_session
def match_db_to_view(matches: Match):
    matches_info = [MatchInfo.from_orm(m) for m in matches]
    all_robots_joined = []
    info_and_robots = []

    for m in matches:
       all_robots_joined.append(len(m.robots_joined))

    for i in range(0, len(matches_info)):
        info_and_robots.append(
            ShowMatch(match_id=matches_info[i].match_id,
                      name=matches_info[i].name,
                      creator_user=matches_info[i].creator_user,
                      max_players=matches_info[i].max_players,
                      robots_joined=all_robots_joined[i]))

    return info_and_robots