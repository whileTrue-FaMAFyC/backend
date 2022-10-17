from fastapi import HTTPException
from base64 import b64decode
import os

BOT_NAME_EXCEPTION = HTTPException(
    status_code=409,
    detail="User already has a bot with this name."
)

ROBOT_DB_EXCEPTION = HTTPException(
    status_code=500,
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
    