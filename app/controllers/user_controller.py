from fastapi import APIRouter
from fastapi.responses import JSONResponse

from database.dao.user_dao import get_user_by_username_or_email
from utils.user_utils import generate_token, TokenData
from validators.user_validators import authenticate_user
from view_entities.user_view_entity import UserLogin

user_controller = APIRouter()

# LOGIN
# Get credentials (username or email and password) and check if they are correct
# If they are, return token. If not, raise HTTP exception
@user_controller.post("/login")
async def login_for_access_token(login_data: UserLogin):
     # Check credentials
    authenticate_user(login_data.username_or_email, login_data.password) 
    user = get_user_by_username_or_email(login_data.username_or_email)     
    # Credentials are OK, generate token and return it
    access_token = generate_token(
        TokenData(username=user.username, email=user.email)
    )
    return JSONResponse(content={"Authorization": access_token})
