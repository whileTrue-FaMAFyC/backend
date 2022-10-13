from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from validators.user_validator import *
from pony.orm import db_session
from view_entities.user_view_entity import UserBase, UserFromDb, UserLogin
from database.models.models import User
from utils.user_utils import *
from random import randint, getrandbits

SECRET_KEY = "2c329a8eca7d0c2ff68d261ad0b2e3efa66cc2603183fe6d0b4b219a11138c84"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440 # One day

user_controller = APIRouter()

# LOGIN
# Get credentials (username or email and password) and check if they are correct
# If they are, return token. If not, raise HTTP exception
@user_controller.post("/login")
async def login_for_access_token(login_data: UserLogin):
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
    return JSONResponse(content="",headers={"Authorization": access_token})