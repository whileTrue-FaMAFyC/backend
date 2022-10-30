from fastapi import HTTPException, status
from pony.orm import db_session, left_join

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

# def parse_b64_source_code(b64_source_code: str):
#     without_prefix = b64_source_code.replace('data:text/x-python;base64,', '')
#     source_code = b64decode(without_prefix).decode()
#     return source_code

# Create new file in user directory
# def create_bot_file(username: str, bot_filename: str, source_code: str):
#     if os.path.exists(f'../robots/{username}'):
#         # If directory already exists for username, just add the new file to it
#         pass
#     else:
#         os.mkdir(f'../robots/{username}')
#     # Create the file
#     f = open(f'../robots/{bot_filename}', 'w')
#     f.write(source_code)

# Transforms the robots selected from the database to the format that will be
# sent to the frontend.
@db_session
def robot_db_to_view(robots: Robot):
    robots_names = [RobotName.from_orm(r) for r in robots]
    return robots_names


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
def get_robot_in_match(match_id: int, abandoning_username: str):
    
    return left_join(
        (r)
        for m in Match for r in m.robots_joined
        if m.match_id == match_id and
           r.owner == User.get(username=abandoning_username)
        )