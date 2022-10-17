from utils.user_utils import INVALID_TOKEN_EXCEPTION
from database.dao.user_dao import *
from jose import jwt

SECRET_KEY = "2c329a8eca7d0c2ff68d261ad0b2e3efa66cc2603183fe6d0b4b219a11138c84"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440 # One day

# Check if token is valid by trying to decode it. If it isn't, raise an exception.
# NOTE: jwt.decode() raises an exception if the token passed is invalid
def validate_token(token: str):
    try:
        jwt.decode(token, SECRET_KEY, ALGORITHM)
    except:
        raise INVALID_TOKEN_EXCEPTION