from fastapi import APIRouter, status

from validators.user_validators import *
from view_entities.user_view_entities import *
from database.dao.user_dao import *

user_controller = APIRouter()

@user_controller.put("/verifyuser/{username}", status_code=status.HTTP_200_OK)
def verify_user(username: str, code: UserVerificationCode):
    user_verification_validator(username, code.verification_code)

    if update_user_verification(username): # Check if updating the verified attribute had any problems.
        return UserFromDb.from_orm(get_user_by_username(username)) # Returns user_info.

    else:
        raise ERROR_UPDATING_USER_DATA
