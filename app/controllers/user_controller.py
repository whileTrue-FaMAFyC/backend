from fastapi import APIRouter, status, HTTPException
from app.validators.user_validator import *
from view_entities.user_view_entities import *
from database.dao.user_dao import *
from passlib.context import CryptContext
from random import randint

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_controller = APIRouter()

@user_controller.post("/signup", status_code=status.HTTP_201_CREATED)
async def sign_up_post(user: UserSignUpData):
    if not validate_email_format(user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="email not valid")

    if not validate_password(user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="password format not valid")
    
    if not validate_username_not_in_use(user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username already in use")
    
    if not validate_email_not_in_use(user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="email already associated with another user")

    encrypted_password = pwd_context.hash(user.password)

    verification_code = randint(100000,999999)

    user_to_db = NewUserToDb(username=user.username, email=user.email, avatar=user.avatar,
                             hashed_password=encrypted_password, verification_code=verification_code,
                             verified=False)

    # Sends the email with the verification code.
    if not send_verification_email(user.email, verification_code):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="internal error sending the email with the verification code")

    # Calls dao function to insert the user into the db
    if not create_user(user_to_db):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="internal error when inserting the user into the database")
    else:
        return user_to_db

# # For testing
# @user_controller.get("/users")
# def get_users():
#     return get_users_db()
