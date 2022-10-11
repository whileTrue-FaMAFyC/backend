from typing import Union
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.hash import bcrypt
from pony.orm import db_session
from fastapi import HTTPException
from database.crud.user import *
from pydantic import BaseModel
from database.crud import user

SECRET_KEY = "2c329a8eca7d0c2ff68d261ad0b2e3efa66cc2603183fe6d0b4b219a11138c84"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440 # One day

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=401,
    detail="Invalid credentials",
)

NOT_VERIFIED_EXCEPTION = HTTPException(
    status_code=401,
    detail="Not verified user",
)

USERNAME_ALREADY_IN_USE_EXCEPTION = HTTPException(
    status_code=409,
    detail="Username already in use"
)

EMAIL_ALREADY_IN_USE_EXCEPTION = HTTPException(
    status_code=409,
    detail="Email already in use"
)

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.verify(plain_password, hashed_password)

@db_session
def authenticate_user(username_or_email: str, password: str):
    # If user logged in with username
    user = get_user_by_username(username_or_email)
    # If user logged in with email
    if not user:
        user = get_user_by_email(username_or_email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Pydantic Model that will be used in the token endpoint for the response
class Token(BaseModel):
    access_token: str

# Dejar esta clase y pasarla como parámetro a generate_token  
class TokenData(BaseModel):
    username: Union[str, None] = None
    email: Union[str, None] = None

# Utility function to generate a token that representes 'data'
def generate_token(data: TokenData):
    data_to_encode = data.dict()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp": expire})
    token = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token