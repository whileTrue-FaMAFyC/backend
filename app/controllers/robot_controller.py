from fastapi import APIRouter, Header, status, UploadFile, Form, File
from jose import jwt
from typing import Union

from database.dao.robot_dao import *
from utils.robot_utils import *
from validators.robot_validators import validate_new_bot
from validators.user_validators import validate_token, SECRET_KEY
from view_entities.robot_view_entities import BotCreate


robot_controller = APIRouter()


# Create new bot
@robot_controller.post("/create-bot", status_code=status.HTTP_200_OK)
async def create_bot(
    authorization: Union[str, None] = Header(None), 
    bot_data: BotCreate = Form(),
    bot_avatar: Union[UploadFile, None] = File()
):
    validate_token(authorization)
    
    # Token is valid, now decode it to get payload
    token_data = jwt.decode(authorization, SECRET_KEY)
    
    owner_username = token_data['username']
    
    validate_new_bot(owner_username, bot_data.name)
    print(bot_avatar == None)
    if bot_avatar:
        print(bot_avatar.content_type)
        contents = await bot_avatar.read()
        file_extension = bot_avatar.filename.split('.')[1].lower()
        # Saves the file in disk and returns its path
        avatar_path = save_bot_avatar(owner_username, bot_data.name, contents, file_extension)

    if not create_new_bot(owner_username, bot_data, avatar_path if bot_avatar else 'default'):
        raise ROBOT_DB_EXCEPTION
    
    return True


@robot_controller.get("/list-robots", status_code=status.HTTP_200_OK)
async def get_matches(authorization: Union[str, None] = Header(None)):
   validate_token(authorization)

    # Token is valid, now decode it to get payload
   token_data = jwt.decode(authorization, SECRET_KEY)
   
   username = token_data['username']
   
   robots_db = get_bots_by_owner(username)
   
   robots_view = robot_db_to_view(robots_db)
   
   return robots_view
