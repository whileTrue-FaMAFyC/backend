from pony.orm import db_session, select

from database.dao.user_dao import get_user_by_username
from database.models.models import Robot
from utils.robot_utils import insert_filename_to_file
from view_entities.robot_view_entities import BotCreate


@db_session 
def get_bot_by_owner_and_name(owner_username: str, bot_name: str):
    return Robot.get(owner=get_user_by_username(owner_username), name=bot_name)

# The exsitance and validation of the username was previously validated,
# i.e. for this function we can assume that the user exists and is verified
@db_session
def create_new_bot(owner_username: str, bot_data: BotCreate):
    try:
        Robot(
            name=bot_data.name,
            source_code=insert_filename_to_file(
                bot_data.source_code, 
                bot_data.bot_filename
            ),
            owner=get_user_by_username(owner_username),
            avatar=bot_data.avatar
        )
        return True
    except:
        return False


@db_session 
def get_bots_by_owner(owner_username: str):
    return Robot.select(owner=get_user_by_username(owner_username))

# @db_session 
# def get_bots_id_by_owner(owner_username: str):
#     return select(r.robot_id for r in Robot if
#                   r.owner == get_user_by_username(owner_username))

@db_session
def get_source_code_by_id(robot_id: int):
    return Robot[robot_id].source_code