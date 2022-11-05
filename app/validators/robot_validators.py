from database.dao.robot_dao import get_bot_by_owner_and_name
from utils.robot_utils import *

# Checks if 'username' already has a bot named 'bot_name'
def new_bot_validator(owner_username: str, bot_name: str):
    valid = get_bot_by_owner_and_name(owner_username, bot_name)
    # If valid is not None, it means that 'user' already has a bot named 'bot_name'
    if valid is not None:
        raise BOT_NAME_EXCEPTION
    
def bot_avatar_validator(avatar_content_type: str):
    if not avatar_content_type.startswith('image/'):
        raise AVATAR_FORMAT_NOT_VALID
    
def bot_source_code_validator(source_code_content_type: str):
    if source_code_content_type == None:
        raise NOT_SOURCE_CODE
    
    if source_code_content_type not in ['application/x-python-code', 'text/x-python']:
        raise SOURCE_CODE_FORMAT_NOT_VALID