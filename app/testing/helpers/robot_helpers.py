from pony.orm import db_session
from pydantic import BaseModel

from database.dao.user_dao import get_user_by_email, get_user_by_username
from database.models.models import Robot


class NewRobot(BaseModel):
    name: str
    email: str
    avatar: str = ""
    source_code: str


@db_session
def create_robot(robot: NewRobot):
    try:
        Robot(
            name=robot.name,
            owner=get_user_by_email(robot.email),
            avatar=robot.avatar,
            source_code=robot.source_code
        )
        return True
    except:
        return False


@db_session
def get_robot_id_by_owner_and_name(owner: str, name: str):
    return Robot.get(owner=get_user_by_username(owner), name=name).robot_id
