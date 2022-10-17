from database.dao.robot_dao import get_bot_by_owner_and_name
from utils.robot_utils import BOT_NAME_EXCEPTION

# Checks if 'username' already has a bot named 'bot_name'
def validate_new_bot(owner_username: str, bot_name: str):
    valid = get_bot_by_owner_and_name(owner_username, bot_name)
    # If valid is not None, it means that 'user' already has a bot named 'bot_name'
    if valid is not None:
        raise BOT_NAME_EXCEPTION