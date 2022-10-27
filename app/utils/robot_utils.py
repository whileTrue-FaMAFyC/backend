from fastapi import HTTPException, status
# import os
from pony.orm import db_session

from database.models.models import Robot
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
    users_robots = [ShowRobot.from_orm(r) for r in robots]
    return users_robots


def insert_filename_to_file(file: str, filename: str):
    if file == "":
        return ""
    return "name:" + filename + ";" + file
