from jose import jwt
from validate_email_address import validate_email

from database.dao.user_dao import *
from utils.user_utils import *
from view_entities.user_view_entities import *

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


def load_avatar_validator(username: str, avatar: UserAvatar):
    user_in_db = get_user_by_username(username)
    if user_in_db is None:
        raise USER_NOT_REGISTERED

    # User not yet verified.
    if not user_in_db.verified:
        raise NOT_VERIFIED_EXCEPTION

    # Checks that the link is not being used for a second time.
    if user_in_db.avatar != "":
        raise AVATAR_ALREADY_LOADED

    if not avatar.avatar.startswith("data:image/") and avatar.avatar != "":
        raise AVATAR_FORMAT_NOT_VALID

def password_restore_request_validator(user: UserIDs):
    user_in_db = get_user_by_username_and_email(user.username, user.email)

    if not user_in_db:
        raise INEXISTENT_USERNAME_EMAIL_COMBINATION

    # User not yet verified.
    if not user_in_db.verified:
        raise NOT_VERIFIED_EXCEPTION

def password_restore_validator(info: RestoreInfo):
    user_in_db = get_user_by_username_or_email(info.email)

    if not user_in_db:
        raise USER_NOT_REGISTERED

    # User not yet verified.
    if not user_in_db.verified:
        raise NOT_VERIFIED_EXCEPTION

    if user_in_db.restore_password_code != info.restore_password_code:
        raise INVALID_RESTORE_CODE

    if not is_valid_password(info.new_password):
        raise PASSWORD_FORMAT_NOT_VALID

def change_password_validator(username: str, data: PasswordChange):
    user = get_user_by_username(username)
    # User doesn't exist in database
    if not user:
        raise INEXISTENT_USER_EXCEPTION

    # Current password is different from the one in the database
    if not verify_password(data.current_password, user.hashed_password):
        raise CREDENTIALS_EXCEPTION

    # New password doesn't satisfy password format requirements
    if not is_valid_password(data.new_password):
        raise PASSWORD_FORMAT_NOT_VALID

    # New password and its confirmation don't match
    if data.new_password != data.new_password_confirmation:
        raise PASSWORD_CONFIRMATION_NOT_MATCH

    # New password is the same as the current one (already checked that the
    # current password matches with the one in the database)
    if data.current_password == data.new_password:
        raise INVALID_NEW_PASSWORD
