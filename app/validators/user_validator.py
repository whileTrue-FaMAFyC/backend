from database.dao.user_dao import *

def validate_user_registered(username: str):
    return get_user_by_username(username) is not None

def validate_user_not_verified(username: str):
    return get_user_by_username(username).verified == False

def validate_verification_code(username: str, code: int):
    return get_user_by_username(username).verification_code == code