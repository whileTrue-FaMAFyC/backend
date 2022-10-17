from pony.orm import db_session, select, delete

from database.dao import user_dao
from database.models.models import Robot, User
from view_entities import robot_view_entities

# Queries
@db_session
def get_robot_by_name_and_user(robot_name: str, owner_username: str):
    robots = Robot.get(owner=User.get(username=owner_username), 
                       name=robot_name)
    return robots
