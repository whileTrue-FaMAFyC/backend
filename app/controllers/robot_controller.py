from fastapi import APIRouter, Header
from jose import jwt
from typing import Union

from database.dao.robot_dao import *
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
    create_new_bot(owner_username, bot_data)
    return bot_data