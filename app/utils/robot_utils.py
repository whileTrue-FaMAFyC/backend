from fastapi import HTTPException, status
from pony.orm import db_session

from database.models.models import Robot, Match
from view_entities.robot_view_entities import *


BOT_NAME_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User already has a robot with this name."
)

ROBOT_DB_EXCEPTION = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal error when creating the new robot in the database."
)

ERROR_INSERTING_ROBOTS = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal error when adding the default robots."
)


# Transforms the robots selected from the database to the format that will be
# sent to the frontend.
@db_session
def robot_db_to_view(robots: Robot):
    return [ShowRobot.from_orm(r) for r in robots]


def insert_filename_to_file(file: str, filename: str):
    if file == "":
        return ""
    return "name:" + filename + ";" + file


# @db_session
# def get_player_in_match(match: AbandonMatch, abandoning_username: str):

#     query = left_join(
#         (r.owner)
#         for m in Match for r in m.robots_joined
#         if m.name == match.name and
#            m.creator_user == User.get(username=match.creator_user) and
#            r.owner == User.get(username=abandoning_username)
#     )
#     print("\n")
#     query.show()
#     return query


@db_session
def get_robot_in_match_by_owner(match_id: int, owner_username: str):

    match = Match[match_id]
    for r in match.robots_joined:
        if r.owner.username == owner_username:
            return r

    return None
