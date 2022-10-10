from fastapi import HTTPException, status
from pydantic import BaseModel, validator
from typing import Union
from email_validator import validate_email, EmailNotValidError
from utils.user import *

class UserBase(BaseModel):
    username: str
    email: str
    avatar: Union[bytes, None] = None

# To parse the parameters of the post request
class UserSignUpData(UserBase):
    password: str

    @validator('email')
    def validate_email_format(cls, email):
        try:
            v = validate_email(email)
        except EmailNotValidError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="email not valid")
        return email
    
    @validator('password')
    def validate_password(cls, password):
        if not is_valid_password(password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="password format not valid")
        return password
    
    @validator('avatar')
    def validate_avatar(cls, avatar):
        pass

# To insert a user to the database
class NewUserToDb(UserBase):
    hashed_password: str
    verification_code: int
    verified: bool

# To get a user from the database. Missing attributes: robots and matches_created
class UserFromDb(UserBase):
    hashed_password: str
    verification_code: int
    verified: bool

    class Config:
        orm_mode = True

