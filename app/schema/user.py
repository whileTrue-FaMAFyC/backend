from fastapi import HTTPException, status
from pydantic import BaseModel, validator
from typing import Union
from email_validator import validate_email, EmailNotValidError

def is_valid_password(password):
    l, u, d = 0, 0, 0
    if (len(password) >= 8):
        for i in password:
            # counting lowercase alphabets
            if (i.islower()):
                l+=1 
            # counting uppercase alphabets
            if (i.isupper()):
                u+=1
            # counting digits
            if (i.isdigit()):
                d+=1
    
    return (l>=1 and u>=1 and d>=1 and l+u+d==len(password))
    
class UserBase(BaseModel):
    username: str
    email: str
    avatar: Union[bytes, None] = None
    password: str

# To parse the parameters of the post request
class UserSignUpData(UserBase):
    
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
    verification_code: int
    verified: bool

# To get a user from the database. Missing attributes: robots and matches_created
class UserFromDb(UserBase):
    verification_code: int
    verified: bool

    class Config:
        orm_mode = True

