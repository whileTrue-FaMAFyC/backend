from fastapi import APIRouter, status
from schema.user import *
from database.crud.user import *
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_router = APIRouter()

@user_router.put("/verifyuser/{username}", status_code=status.HTTP_200_OK)
def verify_user(username: str, code: UserVerificationCode):
    user_from_db = get_user_by_username(username)
    
    if user_from_db == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="user not registered")
    
    if user_from_db.verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="user already verified")
    
    elif code.verification_code != user_from_db.verification_code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="wrong verification code")
    
    elif update_user_verification(username=username): # Check if updating the verified attribute had any problems.
        return UserFromDb.from_orm(get_user_by_username(username)) # Returns user_info.
    
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="internal error when updating the user info in the database")
