from database.models.models import Robot, User
from pony.orm import db_session

@db_session
# Returns True if the user with username `creator_username` has a robot
# with name `robot_name` in it's library. False otherwise. 
def belongs_to_user(robot_name: str, creator_username:str):
    robots = Robot.get(owner = User.get(username=creator_username), 
                       name = robot_name)
    return robots