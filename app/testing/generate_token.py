from fastapi import HTTPException
from datetime import datetime, timedelta
from jose import jwt
from passlib.hash import bcrypt
from pydantic import BaseModel

SECRET_KEY = "2c329a8eca7d0c2ff68d261ad0b2e3efa66cc2603183fe6d0b4b219a11138c84"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440 # One day

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

MOCK_TOKEN_JULI = generate_token(
    TokenData(
        username='jolcese', 
        email='juliolcese@gmail.com'
    )
)

MOCK_TOKEN_VALEN = generate_token(
    TokenData(
        username='valennegrelli', 
        email='valen57negrelli@yahoo.com.ar'
    )
)

MOCK_TOKEN_BENJA = generate_token(
    TokenData(
        username='basbenja', 
        email='basbenja@gmail.com'
    )
)

MOCK_TOKEN_TONI = generate_token(
    TokenData(
        username='tonimond', 
        email='tonimondejar@gmail.com'
    )
)

print(MOCK_TOKEN_JULI)