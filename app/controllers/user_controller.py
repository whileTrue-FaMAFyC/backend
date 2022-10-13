from fastapi import APIRouter, status, HTTPException
from validators.user_validator import *
from view_entities.user_view_entities import *
from database.dao.user_dao import *

user_controller = APIRouter()

@user_controller.put("/verifyuser/{username}", status_code=status.HTTP_200_OK)
def verify_user(username: str, code: UserVerificationCode):
    
    if not validate_user_registered(username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="user not registered")
    
    if not validate_user_not_verified(username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="user already verified")

    if not validate_verification_code(username, code.verification_code):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="wrong verification code")
    
    if update_user_verification(username): # Check if updating the verified attribute had any problems.
        return UserFromDb.from_orm(get_user_by_username(username)) # Returns user_info.
    
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="internal error when updating the user info in the database")
