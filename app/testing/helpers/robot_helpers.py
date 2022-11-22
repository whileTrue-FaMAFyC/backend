from pony.orm import db_session
from pydantic import BaseModel

from database.dao.user_dao import get_user_by_username
from database.models.models import Robot


@db_session
def get_robot_id_by_owner_and_name(owner: str, name: str):
    return Robot.get(owner=get_user_by_username(owner), name=name).robot_id
