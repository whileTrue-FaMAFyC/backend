from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from pony.orm import db_session
from pydantic import BaseModel
from schema.user import UserBase, UserFromDb, UserLogIn
from database.models import User
from utils.user import *
from random import randint, getrandbits

SECRET_KEY = "2c329a8eca7d0c2ff68d261ad0b2e3efa66cc2603183fe6d0b4b219a11138c84"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440 # One day

user_router = APIRouter()

# FUNCTION JUST TO TEST THE BASIC FUNCTIONALITY (THEN DELETE IT)
# CREATE USER
@user_router.post('/users', response_model=UserFromDb)
async def create_user(user: UserBase):
    with db_session:
        if get_user_by_username(user.username) is not None:
            raise USERNAME_ALREADY_IN_USE_EXCEPTION
        elif get_user_by_username(user.username) is not None:
            raise EMAIL_ALREADY_IN_USE_EXCEPTION
        user_obj = User(
            username=user.username,
            email=user.email,
            avatar=None,
            hashed_password=bcrypt.hash(user.hashed_password),
            verification_code=randint(1000,9999),
            verified=bool(getrandbits(1))
        )
        return UserFromDb.from_orm(user_obj)

# LOGIN
# Get credentials (username or email and password) and check if they are correct
# If they are, return token. If not, raise HTTP exception
@user_router.post("/login", response_model=Token)
async def login_for_access_token(login_data: UserLogIn):
     # Check credentials
    user = authenticate_user(login_data.username_or_email, login_data.password)
    if not user:
        raise CREDENTIALS_EXCEPTION
    if not user.verified:
        raise NOT_VERIFIED_EXCEPTION
    # Credentials are OK, generate token and return it
    access_token = generate_token(
        TokenData(user=user.username, email=user.email)
    )
    return Token(access_token=access_token)