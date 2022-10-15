from pony.orm import db_session
from database.models.models import User

@db_session
def get_user_by_username(username: str):
    return User.get(username=username)

@db_session
def get_user_by_email(email: str):
    return User.get(email=email)