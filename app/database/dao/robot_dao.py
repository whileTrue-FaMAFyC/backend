from database.models.models import Robot, User
from database.dao import user_dao
from view_entities import robot_view_entities
from pony.orm import db_session

@db_session
def create_robot(robot: robot_view_entities.NewRobotView):
    try:
        Robot(name=robot.name, owner = user_dao.get_user_by_email(robot.email), 
              avatar = robot.avatar, source_code = robot.source_code.filename)
        return True
    except:
        return False

@db_session
def get_robot_from_user(owner_name: str, robot_name:str):
    robot = Robot.get(owner = User.get(username=owner_name), name=robot_name)
    return robot