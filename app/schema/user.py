from fastapi import HTTPException, UploadFile, status
from pydantic import BaseModel, validator
from typing import Union
import email_validator
from utils.user import *

class UserBase(BaseModel):
    username: str
    email: str
    avatar: Union[UploadFile, None] = None

# To parse the parameters of the post request
class UserSignUpData(UserBase):
    password: str

    @validator('email')
    def validate_email_format(cls, email):
        try:
            # Checks the syntax of the email. Needs the email_validator module prefix for issues
            #  with another function of utils/user.py.
            v = email_validator.validate_email(email)
        except email_validator.EmailNotValidError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="email not valid")
        return email
    
    @validator('password')
    def validate_password(cls, password):
        if not is_valid_password(password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="password format not valid")
        return password
    
    @validator('avatar')
    def validate_avatar(cls, avatar):
        if avatar is not None:
            if avatar.content_type != "image/png":
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="avatar format not valid")
        return avatar

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

