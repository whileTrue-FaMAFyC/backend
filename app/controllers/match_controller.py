from database.dao import match_dao
from fastapi import APIRouter, HTTPException, status, Header
from validators.match_validators import new_match_validator
from view_entities.match_view_entities import NewMatch
from validators.user_validators import validate_token, SECRET_KEY
from utils.user_utils import *
from jose import jwt
from typing import Union

match_controller = APIRouter(prefix="/matches")

# @match_controller.post("/new-match", status_code = status.HTTP_201_CREATED)
# async def create_match(new_match: NewMatch):
#     new_match_validator(new_match)  


#     created = match_dao.create_new_match(new_match)
    
#     if not created:
#         raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             detail = "Internal error creating the match" )
#     return True

@match_controller.post("/new-match", status_code = status.HTTP_201_CREATED)
async def create_match(new_match: NewMatch, authorization: Union[str, None] = Header(None)):
    
    validate_token(authorization)
    token_data = jwt.decode(authorization, SECRET_KEY)
    creator_username = token_data['username']
    
    new_match_validator(creator_username, new_match)  
    created = match_dao.create_new_match(creator_username, new_match)
    
    if not created:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail = "Internal error creating the match" )
    return True