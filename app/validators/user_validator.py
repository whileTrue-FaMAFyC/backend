from database.dao.user_dao import *
from fastapi import HTTPException, status

def user_verification_validator(username: str, code: int):
    user_in_db = get_user_by_username(username) 
    if user_in_db is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="user not registered")
    if user_in_db.verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="user already verified")
    if user_in_db.verification_code != code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="wrong verification code")
