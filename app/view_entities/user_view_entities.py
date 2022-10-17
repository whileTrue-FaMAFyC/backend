from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    avatar: str = ""

class NewUserToDb(UserBase):
    hashed_password: str
    verification_code: int
    verified: bool