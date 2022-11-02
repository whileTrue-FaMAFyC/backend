from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    avatar: str = 'default'

# To parse the parameters of the post request
class UserSignUpData(UserBase):
    password: str

# To receive the login data
class UserLogin(BaseModel):
    username_or_email: str
    password: str
    
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

# To show in list matches
class UserInMatch(BaseModel):
    username: str
    
    class Config:
        orm_mode = True

# To parse user avatar
class UserAvatar(BaseModel):
    avatar: str