from fastapi import HTTPException, UploadFile, status
from pydantic import BaseModel, validator
from typing import Union
from email_validator import validate_email, EmailNotValidError
from utils.user import *

### To parse request body always use a pydantic schema


class UserBase(BaseModel):
    username: str
    email: str
    avatar: Union[UploadFile, None] = None

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

# To parse the request body of the verify user endpoint
class UserVerificationCode(BaseModel):
    verification_code: int
