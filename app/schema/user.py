from pydantic import BaseModel, EmailStr

# To insert the user to the database, no se si hace falta
# class User:
#     username: str

# To parse the parameters of the post request
class UserSignUp(BaseModel):
    username: str
    email: EmailStr
    avatar: bytes # not sure
    password: str
