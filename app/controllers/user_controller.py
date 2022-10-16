from fastapi import APIRouter, status
from passlib.hash import bcrypt
from random import randint

from database.dao.user_dao import *
from validators.user_validators import *
from view_entities.user_view_entities import *

user_controller = APIRouter()

@user_controller.post("/signup", status_code=status.HTTP_201_CREATED)
async def sign_up_post(user: UserSignUpData):
    sign_up_validator(user)

    encrypted_password = bcrypt.hash(user.password)

    verification_code = randint(100000,999999)

    avatar_file = insert_filename_to_file(user.avatar, user.avatarFilename)

    user_to_db = NewUserToDb(username=user.username, email=user.email,
                            avatar=avatar_file, hashed_password=encrypted_password,
                            verification_code=verification_code, verified=False)

    # Sends the email with the verification code.
    if not send_verification_email(user.email, verification_code):
        raise ERROR_SENDING_VERIFICATION_EMAIL
    
    # Calls dao function to insert the user into the db
    if not create_user(user_to_db):
        raise ERROR_INSERTING_DATA
    else:
        return user_to_db

@user_controller.put("/verifyuser/{username}", status_code=status.HTTP_200_OK)
def verify_user(username: str, code: UserVerificationCode):
    user_verification_validator(username, code.verification_code)

    if update_user_verification(username): # Check if updating the verified attribute had any problems.
        return UserFromDb.from_orm(get_user_by_username(username)) # Returns user_info.

    else:
        raise ERROR_UPDATING_USER_DATA