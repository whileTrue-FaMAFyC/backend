from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    avatar: str = ""


# To parse the parameters of the post request
class UserSignUpData(UserBase):
    password: str


# To receive the login data
class UserLogin(BaseModel):
    username_or_email: str
    password: str


# To return token and avatar upon succesful login
class LoginData(BaseModel):
    authorization: str
    avatar: str


# To insert a user to the database
class NewUserToDb(UserBase):
    hashed_password: str
    verification_code: int
    verified: bool


# To get a user from the database. Missing attributes: robots and
# matches_created
class UserFromDb(UserBase):
    hashed_password: str
    verification_code: int
    verified: bool

    class Config:
        orm_mode = True


# To parse the request body of the verify user endpoint
class UserVerificationCode(BaseModel):
    verification_code: int


# To change password
class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    new_password_confirmation: str


# To show in list matches
class UserInMatch(BaseModel):
    username: str

    class Config:
        orm_mode = True


# To parse user avatar
class UserAvatar(BaseModel):
    avatar: str


class JoinMatchUser(BaseModel):
    username: str
    avatar: str


class UserIDs(BaseModel):
    username: str
    email: str


class RestoreInfo(BaseModel):
    email: str
    new_password: str
    restore_password_code: int
