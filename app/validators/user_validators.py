from jose import jwt
from validate_email_address import validate_email

from database.dao.user_dao import *
from utils.user_utils import *
from view_entities.user_view_entities import UserSignUpData

def sign_up_validator(user: UserSignUpData):
    # Email format validator
    if not validate_email(user.email):
        raise EMAIL_NOT_VALID
    
    # Email exists validator
    is_valid = validate_email(user.email, verify=True)
    if not is_valid or is_valid == None:
        raise EMAIL_NOT_EXISTS

    # Avatar format validator
    if not user.avatar.startswith("data:image/png") and user.avatar != "":
        raise AVATAR_FORMAT_NOT_VALID

    # Password format validator
    if not is_valid_password(user.password):
        raise PASSWORD_FORMAT_NOT_VALID
    
    # Username not in use validator
    if get_user_by_username(user.username) is not None:
        raise USERNAME_ALREADY_IN_USE

    # Email not in use validator
    if get_user_by_email(user.email) is not None:
        raise EMAIL_ALREADY_IN_USE

def user_verification_validator(username: str, code: int):
    user_in_db = get_user_by_username(username) 
    if user_in_db is None:
        raise USER_NOT_REGISTERED
    if user_in_db.verified:
        raise USER_ALREADY_VERIFIED
    if user_in_db.verification_code != code:
        raise WRONG_VERIFICATION_CODE

SECRET_KEY = "2c329a8eca7d0c2ff68d261ad0b2e3efa66cc2603183fe6d0b4b219a11138c84"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440 # One day

def validate_token(token: str):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except:
        raise INVALID_TOKEN_EXCEPTION