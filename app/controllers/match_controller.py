from fastapi import APIRouter, HTTPException, status, Header
from jose import jwt
from typing import Union

from database.dao import match_dao
from utils.match_utils import ERROR_CREATING_MATCH, match_db_to_view
from utils.user_utils import *
from validators.match_validators import new_match_validator, join_match_validator
from validators.user_validators import validate_token, SECRET_KEY
from view_entities.match_view_entities import NewMatch, JoinMatch

match_controller = APIRouter(prefix="/matches")

@match_controller.post("/new-match", status_code=status.HTTP_201_CREATED)
async def create_match(new_match: NewMatch, authorization: Union[str, None] = Header(None)):
    validate_token(authorization)

    token_data = jwt.decode(authorization, SECRET_KEY)
    
    creator_username = token_data['username']
    
    new_match_validator(creator_username, new_match)  
    
    created = match_dao.create_new_match(creator_username, new_match)
    
    if not created:
        raise ERROR_CREATING_MATCH
    return True

@match_controller.get("/list-matches", status_code=status.HTTP_200_OK)
async def get_matches(authorization: Union[str, None] = Header(None)):   
   validate_token(authorization)

   matches_db = match_dao.get_all_matches()
   
   matches_view = match_db_to_view(matches_db)
   
   return matches_view

@match_controller.post("/join-match", status_code=status.HTTP_200_OK)
def join_match(match: JoinMatch, authorization: Union[str, None] = Header(None)):
    validate_token(authorization)

    token_data = jwt.decode(authorization, SECRET_KEY)
    
    joining_user = token_data['username']

    join_match_validator(joining_user, match)

    if not match_dao.update_joining_user_match(joining_user, match):
        raise HTTPException()

    ## SUSCRIBE USER TO WEB SOCKET
    
    return True