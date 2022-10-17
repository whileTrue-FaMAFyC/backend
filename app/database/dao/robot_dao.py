from pony.orm import db_session, select, delete

from database.dao import user_dao
from database.models.models import Robot, User
from view_entities import robot_view_entities

# Creation
@db_session
def create_robot(robot: robot_view_entities.NewRobot):
    try:
        Robot(name=robot.name, owner=user_dao.get_user_by_email(robot.email), 
              avatar=robot.avatar, source_code=robot.source_code)
        return True
    except:
        return False

# Queries
@db_session
def get_robot_by_name_and_user(robot_name: str, owner_username: str):
    robots = Robot.get(owner=User.get(username=owner_username), 
                       name=robot_name)
    return robots

@db_session
def get_robots_by_username(username: str):
    user = User.get(username=username)
    robots = select(r.name for r in Robot if r.owner == user)
    return robots

@db_session
def get_robot_names():
    return select(u.name for u in Robot)

@db_session
def delete_table_robot():
    try:
        delete(p for p in Robot)
        return True
    except:
        return False