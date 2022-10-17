from pony.orm import db_session
from database.models.models import User

@db_session
def delete_user_by_username(username: str):
    try:
        user_in_db = User.get(username=username)
        if user_in_db != None:
            user_in_db.delete()
        return True
    except:
        return False

@db_session
def delete_user_by_email(email: str):
    try:
        user_in_db = User.get(email=email)
        if user_in_db != None:
            user_in_db.delete()
        return True
    except:
        return False