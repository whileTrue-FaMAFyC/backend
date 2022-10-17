from jose import jwt

from database.dao.user_dao import *
from utils.user_utils import INVALID_TOKEN_EXCEPTION

SECRET_KEY = "2c329a8eca7d0c2ff68d261ad0b2e3efa66cc2603183fe6d0b4b219a11138c84"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440 # One day

def validate_token(token: str):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except:
        raise INVALID_TOKEN_EXCEPTION