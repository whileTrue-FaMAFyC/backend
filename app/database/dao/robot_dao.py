from database.dao import user_dao
from database.models.models import Robot, User
from pony.orm import db_session
from view_entities import robot_view_entities

@db_session
def create_robot(robot: robot_view_entities.NewRobot):
    try:
        Robot(name=robot.name, owner = user_dao.get_user_by_email(robot.email), 
              avatar = robot.avatar, source_code = robot.source_code)
        return True
    except:
        return False

@db_session
def get_robot_by_name_and_user(robot_name: str, owner_username: str):
    robots = Robot.get(owner = User.get(username = owner_username), 
                       name = robot_name)
    return robots
