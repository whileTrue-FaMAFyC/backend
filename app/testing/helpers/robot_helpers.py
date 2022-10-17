from pony.orm import db_session
from pydantic import BaseModel

from database.dao.user_dao import get_user_by_email
from database.models.models import Robot

class NewRobot(BaseModel):
    name: str
    email: str
    avatar: str = ""
    source_code: str

# Creation
@db_session
def create_robot(robot: NewRobot):
    try:
        Robot(name=robot.name, owner=get_user_by_email(robot.email), 
              avatar=robot.avatar, source_code=robot.source_code)
        return True
    except:
        return False
    
    