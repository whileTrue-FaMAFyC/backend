from fastapi import HTTPException, status
from pony.orm import db_session

from database.models.models import Match 
from view_entities.match_view_entities import *
from view_entities.robot_view_entities import *


ERROR_CREATING_MATCH = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal error creating the match."
)

NOT_CREATOR = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Only the creator can start the match."
)

MATCH_ALREADY_STARTED = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The match has already started."
)

NOT_ENOUGH_PLAYERS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The minimum amount of players hasn't been reached."
)

INEXISTENT_MATCH = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The match does not exist."
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

@db_session
def match_validator_info(match_id: int):
    match_info = Match[match_id]

    return StartMatchValidator(
        min_players=match_info.min_players,
        started=match_info.started,
        robots_joined=len(match_info.robots_joined),
        creator_username=match_info.creator_user.username
    )