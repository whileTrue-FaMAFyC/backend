from fastapi import APIRouter, Header
from jose import jwt

from database.dao.robot_dao import *
from validators.robot_validators import validate_new_bot
from validators.user_validators import validate_token, SECRET_KEY
from view_entities.robot_view_entities import BotCreate

robot_controller = APIRouter()

# Create new bot (VERSION WITH TOKEN)
@robot_controller.post("/create-bot")
async def create_bot(bot_data: BotCreate):
    validate_token(bot_data.access_token)
    # Token is valid, now decode it to get payload
    token_data = jwt.decode(bot_data.access_token, SECRET_KEY)
    owner_username = token_data['username']
    validate_new_bot(owner_username, bot_data.name)
    create_new_bot(owner_username, bot_data)
    return bot_data

# Create new bot (VERSION WITHOUT TOKEN)
# @robot_controller.post("/create-bot")
# async def create_bot(bot_data: BotCreate):
#     if get_user_by_username(bot_data.owner_username) is None:
#         raise INEXISTENT_USER_EXCEPTION
#     validate_new_bot(bot_data.owner_username, bot_data.name)
#     create_new_bot(bot_data.owner_username, bot_data)
#     return bot_data