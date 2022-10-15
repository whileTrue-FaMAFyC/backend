from fastapi import APIRouter, status
from database.dao import match_dao
from utils.match_utils import match_db_to_view

controller = APIRouter(prefix="/matches")

@controller.get("/list-matches", status_code = status.HTTP_200_OK)
async def get_matches():
   matches_db = match_dao.get_all_matches()
   matches_view = match_db_to_view(matches_db)
   return matches_view