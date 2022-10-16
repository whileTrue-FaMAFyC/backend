from utils.user_utils import *
from database.dao.user_dao import *

def user_verification_validator(username: str, code: int):
    user_in_db = get_user_by_username(username) 
    if user_in_db is None:
        raise USER_NOT_REGISTERED
    if user_in_db.verified:
        raise USER_ALREADY_VERIFIED
    if user_in_db.verification_code != code:
        raise WRONG_VERIFICATION_CODE
