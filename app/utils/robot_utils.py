from fastapi import HTTPException, status
from pony.orm import db_session
import os

from database.models.models import Robot, Match, User
from view_entities.robot_view_entities import *


BOT_NAME_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User already has a bot with this name."
)

ROBOT_DB_EXCEPTION = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal error when creating the new bot in the database."
)

AVATAR_FORMAT_NOT_VALID = HTTPException(
    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    detail="Avatar extension file not supported."
)

SOURCE_CODE_FORMAT_NOT_VALID = HTTPException(
    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    detail="Source code extension is not .py."
)

NOT_SOURCE_CODE = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Source code not entered."
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
    # return left_join(
    #     (r)
    #     for m in Match for r in m.robots_joined
    #     if m.match_id == match_id and
    #        r.owner == User.get(username=owner_username)
    #     )


# Save avatar in assests directory and return the url
def save_bot_avatar(username: str, bot_filename: str, contents: bytes, file_extension: str):
    if os.path.exists(f'../assets/users/{username}'):
        pass
    # Here, the else will execute only if the username didn't upload an avatar
    else:
        os.mkdir(f'../assets/users/{username}')

    # If the file exsists, it will override it. If not, it will create a new one
    f = open(f'../assets/users/{username}/avatar_{bot_filename}.{file_extension}', 'wb')
    f.write(contents)
    f.close()
    return (f'../assets/users/{username}/avatar_{bot_filename}.{file_extension}')


def save_bot_source_code(username: str, bot_filename: str, contents: bytes):
    if os.path.exists(f'../assets/users/{username}'):
        pass
    # Here, the else will execute only if the username didn't upload an avatar
    else:
        os.mkdir(f'../assets/users/{username}')

    # If the file exsists, it will override it. If not, it will create a new one
    f = open(f'../assets/users/{username}/{bot_filename}', 'wb')
    f.write(contents)
    f.close()
    return (f'../assets/users/{username}/{bot_filename}')
