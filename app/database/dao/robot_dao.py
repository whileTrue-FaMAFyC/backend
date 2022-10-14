from database.models.models import Robot, User
from database.dao import user_dao
from view_entities import robot_view_entities
from pony.orm import db_session, select

@db_session
# Returns True if the user with username `creator_username` has a robot
# with name `robot_name` in it's library. False otherwise. 
def belongs_to_user(robot_name: str, creator_username:str):
    robots = Robot.get(owner = User.get(username=creator_username), 
                       name = robot_name)
    return robots

@db_session
def get_robots_from(usern: str):
    user = User.get(username=usern)
    robots = select(r.name for r in Robot if r.owner == user)
    return robots

@db_session
def get_robotnames():
    return select(u.name for u in Robot)


@db_session
def create_robot(robot: robot_view_entities.NewRobotView):
    try:
        Robot(name=robot.name, owner = user_dao.get_user_by_email(robot.email), 
              avatar = robot.avatar, source_code = robot.source_code.filename)
        return True
    except:
        return False