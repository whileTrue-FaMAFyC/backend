from fastapi import APIRouter, Header, status
from jose import jwt
from typing import Union

from database.dao.robot_dao import *
from utils.robot_utils import ROBOT_DB_EXCEPTION, robot_db_to_view
from validators.robot_validators import validate_new_bot
from validators.user_validators import validate_token, SECRET_KEY
from view_entities.robot_view_entities import BotCreate


robot_controller = APIRouter()

# Create new bot (VERSION WITH TOKEN)
@robot_controller.post("/create-bot")
async def create_bot(
    authorization: Union[str, None] = Header(None), 
    bot_data: BotCreate = None
):
    validate_token(authorization)
    # Token is valid, now decode it to get payload
    token_data = jwt.decode(authorization, SECRET_KEY)
    
    owner_username = token_data['username']
    
    validate_new_bot(owner_username, bot_data.name)
    
    if not create_new_bot(owner_username, bot_data):
        raise ROBOT_DB_EXCEPTION
    
    return bot_data

@robot_controller.get("/list-robots", status_code=status.HTTP_200_OK)
async def get_matches(authorization: Union[str, None] = Header(None)):
   validate_token(authorization)
   token_data = jwt.decode(authorization, SECRET_KEY)
   username = token_data['username']
   robots_db = get_bots_by_owner(username)
   robots_view = robot_db_to_view(robots_db)
   return robots_view