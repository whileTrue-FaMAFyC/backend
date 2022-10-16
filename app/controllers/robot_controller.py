from fastapi import APIRouter, HTTPException

from database.dao.robot_dao import *
from utils.user_utils import INEXISTENT_USER_EXCEPTION
from validators.robot_validators import validate_new_bot
from view_entities.robot_view_entities import BotCreate

robot_controller = APIRouter()

# Create new bot (VERSION WITH TOKEN)
# @user_controller.post("/create-bot")
# async def create_bot(token: str, bot_data: BotCreate):
#     validate_token(token)
#     # Token is valid, now decode it to get payload
#     token_data = jwt.decode(token, SECRET_KEY)
#     user = get_user_by_username(token_data['username'])
#     create_new_bot(user, bot_data)
#     return 

# Create new bot (VERSION WITHOUT TOKEN)
@robot_controller.post("/create-bot")
async def create_bot(bot_data: BotCreate):
    if get_user_by_username(bot_data.owner_username) is None:
        raise INEXISTENT_USER_EXCEPTION
    validate_new_bot(bot_data.owner_username, bot_data.name)
    create_new_bot(bot_data.owner_username, bot_data)
    return bot_data