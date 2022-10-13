from typing import Union
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    avatar: Union[bytes, None] = None
    hashed_password: str

class UserLogin(BaseModel):
    username_or_email: str
    password: str

# To get a user from the database. Missing attributes: robots and matches_created
class UserFromDb(UserBase):
    verification_code: int
    verified: bool

    class Config:
        orm_mode = True
        
    
    