from fastapi import APIRouter, status
from validators.user_validators import *
from view_entities.user_view_entities import *
from database.dao.user_dao import *
from passlib.context import CryptContext
from random import randint

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_controller = APIRouter()

@user_controller.post("/signup", status_code=status.HTTP_201_CREATED)
async def sign_up_post(user: UserSignUpData):
    sign_up_validator(user)

    encrypted_password = pwd_context.hash(user.password)

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
