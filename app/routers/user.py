from fastapi import APIRouter, status
from schema.user import *
from database.crud.user import *
from passlib.context import CryptContext
from random import randint

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_router = APIRouter()

# For testing we use the signup endpoint of another branch
@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
def sign_up_post(user: UserSignUpData):
    if get_user_by_username(user.username) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username already in use")
    
    if get_user_by_email(user.email) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="email already associated with another user")

    encrypted_password = pwd_context.hash(user.password)

    verification_code = randint(100000,999999)

    ### SEND VERIFICATION EMAIL

    user_to_db = NewUserToDb(username=user.username, email=user.email, avatar=user.avatar,
                             hashed_password=encrypted_password, verification_code=verification_code,
                             verified=False)
    
    # Calls crud function to insert the user into the db
    if create_user(user_to_db):
        return user_to_db
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="internal error when inserting the user into the database")


@user_router.put("/verifyuser/{username}", status_code=status.HTTP_200_OK)
def verify_user(username: str, code: UserVerificationCode):
    user_from_db = get_user_by_username(username)
    
    if user_from_db.verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="user already verified")
    
    elif code.verification_code != user_from_db.verification_code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="wrong verification code")
    
    elif update_user_verification(username=username): # Check if updating the verified attribute had any problems.
        return UserFromDb.from_orm(get_user_by_username(username)) # Returns user_info.
    
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="internal error when updating the user info in the database")

# # For testing
# @user_router.get("/users")
# def get_users():
#     return get_users_db()
