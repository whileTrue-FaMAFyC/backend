from database.dao.user_dao import *
import jwt

SECRET_KEY = "2c329a8eca7d0c2ff68d261ad0b2e3efa66cc2603183fe6d0b4b219a11138c84"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440 # One day

def validate_token(token: str):
    try:
        token_data = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
        if token_data['verified'] is False:
            return False
        user = get_user_by_username(token_data['username'])
        if user is None:
            return False
        return token_data
    except:
        return False