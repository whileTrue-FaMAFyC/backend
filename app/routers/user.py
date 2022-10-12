from fastapi import APIRouter, status
from schema.user import *
from database.crud.user import *
from passlib.context import CryptContext
from random import randint

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_router = APIRouter()

@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def sign_up_post(user: UserSignUpData):

    if get_user_by_username(user.username) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username already in use")
    
    if get_user_by_email(user.email) is not None: # If the user is not in the database returns None
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

    # Calls crud function to insert the user into the db
    if not create_user(user_to_db):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="internal error when inserting the user into the database")
    else:
        return user_to_db

# # For testing
# @user_router.get("/users")
# def get_users():
#     return get_users_db()
