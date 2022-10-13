from database.dao.user_dao import *
from utils.user_utils import *

def authenticate_user(username_or_email: str, password: str):
    # If user logged in with username
    user = get_user_by_username(username_or_email)
    # If user logged in with email
    if not user:
        user = get_user_by_email(username_or_email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user