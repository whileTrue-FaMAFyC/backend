from database.dao.user_dao import *
from fastapi import HTTPException, status

def validate_user_registered(username: str):
    if get_user_by_username(username) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="user not registered")

def validate_user_not_verified(username: str):
    if get_user_by_username(username).verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="user already verified")

def validate_verification_code(username: str, code: int):
    if get_user_by_username(username).verification_code != code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="wrong verification code")
