from jose import jwt
from validate_email_address import validate_email

from database.dao.user_dao import *
from utils.user_utils import *
from view_entities.user_view_entities import UserAvatar, UserSignUpData

def sign_up_validator(user: UserSignUpData):
    # Email format validator
    if not validate_email(user.email):
        raise EMAIL_NOT_VALID

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

# NOTE: jwt.decode() raises an exception upon invalid token
def validate_token(token: str):
    try:
        jwt.decode(token, SECRET_KEY, ALGORITHM)
    except:
        raise INVALID_TOKEN_EXCEPTION


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

def load_avatar_validator(username: str, content_type: str):
    user_in_db = get_user_by_username(username)
    if user_in_db is None:
        raise USER_NOT_REGISTERED

    # User not yet verified.
    if not user_in_db.verified:
        raise NOT_VERIFIED_EXCEPTION

    # Checks that the link is not being used for a second time.
    if user_in_db.avatar != 'default':
        raise AVATAR_ALREADY_LOADED

    # if not avatar.avatar.startswith("data:image/") and avatar.avatar != "":
    #     raise AVATAR_FORMAT_NOT_VALID
    # REPLACE FOR:
    #   Reasons:
    #       - avatar.avatar != "" already checked in controller by checking that the avatar is not None
    #       - avatar.avatar.startswith("data:image/") can be checked by accessing the content-type of the
    #       UploadFile type-content attribute in the controller
    if not content_type.startswith('image'):
        raise AVATAR_FORMAT_NOT_VALID