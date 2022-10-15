from fastapi import APIRouter, Depends, HTTPException

from view_entities.robot_view_entities import BotCreate
from database.dao.robot_dao import *
from validators.user_validators import *

user_controller = APIRouter()

# Create new bot
@user_controller.post("/create-bot")
async def create_bot(token: str, bot_data: BotCreate):
    valid_token = validate_token(token)
    if not valid_token:
        raise 
    else:
        user = valid_token['username']
        create_new_bot(user, bot_data)
    return 