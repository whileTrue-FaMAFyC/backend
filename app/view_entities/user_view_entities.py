from fastapi import UploadFile
from pydantic import BaseModel
from typing import Union

class UserBase(BaseModel):
    username: str
    email: str
    avatar: Union[UploadFile, None] = None

class NewUserToDb(UserBase):
    hashed_password: str
    verification_code: int
    verified: bool