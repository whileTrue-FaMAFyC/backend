from database.dao import match_dao
from fastapi import APIRouter, HTTPException, status
from validators.match_validators import new_match_validator
from view_entities.match_view_entities import NewMatch
from utils.user_utils import *

match_controller = APIRouter(prefix="/matches")

@match_controller.post("/new-match", status_code = status.HTTP_201_CREATED)
async def create_match(new_match: NewMatch):
    # valid_token = validate_token(token)
    # if not valid_token:
    #     raise 
    # else:
    #     user = valid_token['username']

    # Check if all parameters are valid
    new_match_validator(new_match)  
    
    created = match_dao.create_new_match(new_match)
    
    if not created:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail = "Internal error creating the match" )
    return True