from pony.orm import db_session

from database.models.models import User
from view_entities import user_view_entities

@db_session
def create_user(user: user_view_entities.NewUserToDb):
    try:
        User(username=user.username, email=user.email, avatar=user.avatar,
         hashed_password=user.hashed_password, 
         verification_code=user.verification_code, verified=user.verified)
        return True
    except:
        return False

@db_session
def get_user_by_email(email: str):
    return User.get(email=email)