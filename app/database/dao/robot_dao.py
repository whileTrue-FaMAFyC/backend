from pony.orm import db_session
from backend.app.database.dao.user_dao import get_user_by_username
from backend.app.view_entities.robot_view_entities import BotCreate
from database.models.models import Robot, User

# Checks if 'username' already has a bot named 'bot_name'
# TODO: debería ir en validators esto
@db_session
def check_new_bot(username: str, bot_name: str):
    user_entity = get_user_by_username(username)
    valid_name = Robot.select(name=bot_name, owner=user_entity)
    if valid_name is None:
        return False
    return True

# The exsitance and validation of the username was previously validated,
# i.e. for this function we can assume that the user exists and is verified
@db_session
def create_new_bot(username: str, bot_data: BotCreate):
    owner_entity = get_user_by_username(username)
    # TODO: Debería chequear que el usuario no tenga ya un robot que se llame igual
    Robot(
        name=bot_data.name,
        source_code=bot_data.source_code,
        owner=owner_entity,
        avatar=bot_data.avatar
    )
    

    