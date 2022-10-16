from pydantic import BaseModel
from typing import Union

class UserBase(BaseModel):
    username: str
    email: str
    avatar: str = ""

class NewUserToDb(UserBase):
    hashed_password: str
    verification_code: int
    verified: bool

class UserInMatch(BaseModel):
    username: str
    
    class Config:
        orm_mode = True