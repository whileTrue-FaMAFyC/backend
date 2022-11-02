from fastapi import HTTPException, status
from pony.orm import db_session
import os

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
    return [ShowRobot.from_orm(r) for r in robots]


def insert_filename_to_file(file: str, filename: str):
    if file == "":
        return ""
    return "name:" + filename + ";" + file

# Save avatar in assests directory and return the url
def save_bot_avatar(username: str, bot_name: str, contents: bytes, file_extension: str):
    if os.path.exists(f'../assets/users/{username}'):
        pass
    # Here, the else will execute only if the username didn't upload an avatar
    else:
        os.mkdir(f'../assets/users/{username}')

    # If the file exsists, it will override it. If not, it will create a new one
    f = open(f'../assets/users/{username}/avatar_{bot_name}.{file_extension}', 'wb')
    f.write(contents)
    f.close()
    return (f'../assets/users/{username}/avatar_{bot_name}.{file_extension}')
