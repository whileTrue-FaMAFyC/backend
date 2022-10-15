from fastapi import HTTPException
from datetime import datetime, timedelta
from jose import jwt
from passlib.hash import bcrypt
from pydantic import BaseModel

SECRET_KEY = "2c329a8eca7d0c2ff68d261ad0b2e3efa66cc2603183fe6d0b4b219a11138c84"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440 # One day

# Status code 401 = Unauthorized
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=401,
    detail="Invalid credentials"
)

NOT_VERIFIED_EXCEPTION = HTTPException(
    status_code=401,
    detail="Not verified user"
)

INEXISTENT_USER_EXCEPTION = HTTPException(
    status_code=401,
    detail="Inexistent user"
)

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.verify(plain_password, hashed_password)

class TokenData(BaseModel):
    username: str
    email: str

# Utility function to generate a token that representes 'data'
def generate_token(data: TokenData):
    data_to_encode = data.dict()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp": expire})
    token = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token