from pony.orm import db_session
from database.dao.user_dao import get_user_by_username
from utils.robot_utils import ROBOT_DB_EXCEPTION
from view_entities.robot_view_entities import BotCreate
from database.models.models import Robot

@db_session 
def get_bot_by_owner_and_name(owner_username: str, bot_name: str):
    return Robot.get(owner=get_user_by_username(owner_username), name=bot_name)

# The exsitance and validation of the username was previously validated,
# i.e. for this function we can assume that the user exists and is verified
@db_session
def create_new_bot(owner_username: str, bot_data: BotCreate):
    # First, check if 'user' already has a robot with the same name
    try:
        Robot(
            name=bot_data.name,
            source_code=bot_data.source_code,
            owner=get_user_by_username(owner_username),
            avatar=bot_data.avatar
        )
    except:
        raise ROBOT_DB_EXCEPTION
    

    