from typing import Union
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pony.orm import db_session
from pydantic import BaseModel
from passlib.hash import bcrypt
from schema.user import UserBase, UserFromDb
from database.models import User
from jose import JWTError, jwt

SECRET_KEY = "2c329a8eca7d0c2ff68d261ad0b2e3efa66cc2603183fe6d0b4b219a11138c84"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440 # One day
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

credentials_exception = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

# Pydantic Model that will be used in the token endpoint for the response
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: Union[str, None] = None
    email: Union[str, None] = None

# Utility function to generate a token that representes 'data'
def generate_token(data: dict, expires_delta: Union[timedelta, None] = None):
    data_to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    data_to_encode.update({"exp": expire})
    token = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.verify(plain_password, hashed_password)

@db_session
def authenticate_user(username_or_email: str, password: str):
    user = User.get(username=username_or_email)
    if not user:
        user = User.get(email=username_or_email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

@db_session
def get_user_by_username(username: str):
    user = User.get(username=username)
    if user is not None:
        user_obj = UserBase(
            username=user.username,
            email=user.email,
            avatar=user.avatar,
            hashed_password=user.password
        )
        return user_obj
    else:
        return None

# Utility function to get the current user
@db_session
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        username: str = payload.get('username')
        print(username)
        email: str = payload.get('email')
        print(email)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, email=email)
    except jwt.JWTError:
        raise credentials_exception
    user = get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user

user_router = APIRouter()

# FUNCTION JUST TO TEST THE BASIC FUNCTIONALITY (THEN DELETE IT)
# CREATE USER
@user_router.post('/users', response_model=UserBase)
async def create_user(user: UserBase):
    with db_session:
        user_obj = User(
            username=user.username,
            email=user.email,
            avatar=None,
            password=bcrypt.hash(user.hashed_password),
            verification_code=5555,
            verified=True
        )
    return UserBase(
        username=user.username,
        email=user.email,
        avatar=None,
        hashed_password= bcrypt.hash(user.hashed_password)
    )


@user_router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise credentials_exception
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = generate_token(
        data={"username": user.username, "email": user.email},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@user_router.get("/users/me/", response_model=UserBase)
async def read_users_me(current_user: UserBase = Depends(get_current_user)):
    return UserBase(
        username=current_user.username,
        email=current_user.email,
        avatar=current_user.avatar,
        hashed_password=current_user.hashed_password
    )