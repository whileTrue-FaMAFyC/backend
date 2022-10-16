from pydantic import BaseModel
from utils.user_utils import *

class UserBase(BaseModel):
    username: str
    email: str
    avatar: str = ""

# To parse the parameters of the post request
class UserSignUpData(UserBase):
    password: str
    avatarFilename: str = ""

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

