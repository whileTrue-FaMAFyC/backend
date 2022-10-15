from pony.orm import db_session
from database.models.models import User

@db_session
def get_user_by_username(username: str):
    return User.get(username=username)

@db_session
def get_user_by_email(email: str):
    return User.get(email=email)

@db_session
def get_user_by_username_or_email(username_or_email: str):
    user = get_user_by_username(username_or_email)
    if not user:
        user = get_user_by_email(username_or_email)
    return user
