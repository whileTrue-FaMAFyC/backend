from view_entities import user_view_entities
from database.models.models import User
from pony.orm import db_session, select

@db_session
def get_usernames():
    return select(u.username for u in User)

@db_session
def create_user(user: user_view_entities.NewUserToDb):
    try:
        # Inserts parameter user in to the 'User' table
        User(username=user.username, email=user.email, avatar=user.avatar,
             hashed_password=user.hashed_password,
             verification_code=user.verification_code, verified=user.verified)
        return True
    except:
        return False

@db_session
def get_user_by_email(email: str):
    return User.get(email=email)
