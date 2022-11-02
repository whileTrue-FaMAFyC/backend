from fastapi import APIRouter, status, UploadFile
from fastapi.responses import JSONResponse
from passlib.hash import bcrypt
from random import randint
from typing import Union

from database.dao.user_dao import *
from utils.user_utils import generate_token, TokenData
from validators.user_validators import *
from view_entities.user_view_entities import *

user_controller = APIRouter()

@user_controller.post("/signup", status_code=status.HTTP_201_CREATED)
async def sign_up_post(user: UserSignUpData):
    sign_up_validator(user)

    encrypted_password = bcrypt.hash(user.password)

    verification_code = randint(100000,999999)

    # NOTE: at first, use default avatar, which is ""
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

    # Check if updating the verified attribute had any problems.
    if update_user_verification(username): 
        return True
    else:
        raise ERROR_UPDATING_USER_DATA


@user_controller.post("/load-avatar/{username}", status_code=status.HTTP_200_OK)
async def load_avatar(username: str, avatar: Union[UploadFile, None] = None):
    # User uploaded an avatar
    if avatar:
        load_avatar_validator(username, avatar.content_type)

        contents = await avatar.read()
        file_extension = avatar.filename.split('.')[1].lower()
        # Saves the file in disk and returns its path
        avatar_path = save_user_avatar(username, contents, file_extension)
        
        if update_user_avatar(username, avatar_path):
            return True
        else:
            raise ERROR_UPDATING_USER_DATA
    
    # If user didn´t upload any avatar, don't change the db
    return



# LOGIN
# Get credentials (username or email and password) and check if they are correct
# If they are, return token. If not, raise HTTP exception
@user_controller.post("/login", status_code=status.HTTP_200_OK)
async def login_for_access_token(login_data: UserLogin):
     # Check credentials
    authenticate_user(login_data.username_or_email, login_data.password) 
    
    user = get_user_by_username_or_email(login_data.username_or_email)     
    
    # Credentials are OK, generate token and return it
    access_token = generate_token(
        TokenData(username=user.username, email=user.email)
    )
    
    return JSONResponse(content={"Authorization": access_token})
