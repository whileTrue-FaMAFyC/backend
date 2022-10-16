from fastapi import APIRouter, status, Header
from database.dao import match_dao
from typing import Union
from utils.match_utils import match_db_to_view
from validators.user_validators import validate_token
controller = APIRouter(prefix="/matches")

@controller.get("/list-matches", status_code = status.HTTP_200_OK)
async def get_matches(authorization: Union[str, None] = Header(None)):
   validate_token(authorization)
   matches_db = match_dao.get_all_matches()
   matches_view = match_db_to_view(matches_db)
   return matches_view