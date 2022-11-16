from fastapi import APIRouter, status, Header
from passlib.hash import bcrypt
from random import randint
from typing import Union

from database.dao.robot_dao import add_default_robots
from database.dao.user_dao import *
from utils.robot_utils import ERROR_INSERTING_ROBOTS
from utils.user_utils import generate_token, TokenData
from validators.user_validators import *
from view_entities.user_view_entities import *

user_controller = APIRouter()

@user_controller.post("/signup", status_code=status.HTTP_201_CREATED)
async def sign_up_post(user: UserSignUpData):
    sign_up_validator(user)

    encrypted_password = bcrypt.hash(user.password)

    verification_code = randint(100000,999999)

    user_to_db = NewUserToDb(
        username=user.username,
        email=user.email,
        hashed_password=encrypted_password,
        verification_code=verification_code,
        verified=False
    )

    # Sends the email with the verification code.
    if not send_verification_email(user.email, verification_code):
        raise ERROR_SENDING_VERIFICATION_EMAIL

    # Calls dao function to insert the user into the db
    if not create_user(user_to_db):
        raise ERROR_INSERTING_DATA
    else:
        return True


@user_controller.put("/verifyuser/{username}", status_code=status.HTTP_200_OK)
async def verify_user(username: str, code: UserVerificationCode):
    user_verification_validator(username, code.verification_code)

    if not update_user_verification(username): # Check if updating the verified attribute had any problems.
        raise ERROR_UPDATING_USER_DATA

    if not add_default_robots(username):
        raise ERROR_INSERTING_ROBOTS

    return True

@user_controller.post("/load-avatar/{username}", status_code=status.HTTP_200_OK)
async def load_avatar(username: str, avatar: UserAvatar):
    load_avatar_validator(username, avatar)

    avatar_file = get_avatar_file(avatar.avatar)

    if update_user_avatar(username, avatar_file):
        return True
    else:
        raise ERROR_UPDATING_USER_DATA


@user_controller.post("/login", status_code=status.HTTP_200_OK)
async def login(login_data: UserLogin):
     # Check credentials
    authenticate_user(login_data.username_or_email, login_data.password)

    user = get_user_by_username_or_email(login_data.username_or_email)

    # Credentials are OK, generate token and return it
    access_token = generate_token(
        TokenData(username=user.username, email=user.email)
    )

    return LoginData(
        authorization=access_token,
        avatar=get_user_avatar(user.username)
    )


@user_controller.get("/user-profile", status_code=status.HTTP_200_OK)
async def get_matches(authorization: Union[str, None] = Header(None)):
   validate_token(authorization)
   token_data = jwt.decode(authorization, SECRET_KEY)
   username = token_data['username']
   
   return get_user_info(username)


@user_controller.post("/password-restore-request", status_code=status.HTTP_200_OK)
async def password_restore_request(user: UserIDs):
    
    password_restore_request_validator(user)

    restore_code = randint(100000,999999)

    if not add_password_restore_code(user.username, restore_code):
        raise ERROR_UPDATING_USER_DATA

    if not send_password_restore_mail(user.email, restore_code):
        raise ERROR_SENDING_RESTORE_CODE_MAIL



@user_controller.put("/password-restore", status_code=status.HTTP_200_OK)
async def password_restore(info: RestoreInfo):
    
    password_restore_validator(info)

    username = get_user_by_email(info.email).username
    
    if not update_user_password(username, info.new_password):
        raise ERROR_UPDATING_USER_DATA
    
    if not update_restore_password_code(username):
        raise ERROR_UPDATING_USER_DATA


@user_controller.patch("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    data: PasswordChange,
    authorization: Union[str, None] = Header(None)
):
    validate_token(authorization)
    token_data = jwt.decode(authorization, SECRET_KEY)
    username = token_data['username']

    change_password_validator(username, data)

    if update_user_password(username, data.new_password):
        return True
    else:
        raise ERROR_UPDATING_USER_DATA
