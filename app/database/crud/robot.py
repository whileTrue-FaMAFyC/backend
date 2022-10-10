from pony.orm import db_session
from database.models import User, Robot

@db_session
def belongs_to_user(creator_robot: str, creator_user:str):
    robots = Robot.get(owner = User.get(username=creator_user), name = creator_robot)
    return robots