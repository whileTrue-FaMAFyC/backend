from database.dao.user_dao import get_user_by_username_or_email
from utils.user_utils import *

def authenticate_user(username_or_email: str, password: str):
    user = get_user_by_username_or_email(username_or_email)
    # User doesn't exist in database
    if not user:
        raise INEXISTENT_USER_EXCEPTION
    # User exists but inserted incorrect password
    if not verify_password(password, user.hashed_password):
        raise CREDENTIALS_EXCEPTION
    # User exists, inserted correct password but user is not yet verified
    if not user.verified:
        raise NOT_VERIFIED_EXCEPTION
