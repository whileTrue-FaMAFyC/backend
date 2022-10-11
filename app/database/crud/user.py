from pony.orm import db_session
from database.models import *

@db_session
def get_user_by_username(username: str):
    return User.get(username=username)

@db_session
def get_user_by_email(email: str):
    return User.get(email=email)

    # if user is not None:
    #     user_obj = UserBase(
    #         username=user.username,
    #         email=user.email,
    #         avatar=user.avatar,
    #         hashed_password=user.password
    #     )
    #     return user_obj
    # else:
    #     return None