from fastapi import APIRouter
from database.dao import match_dao
from view_entities.match_view_entity import match_db_to_view

controller = APIRouter(prefix="/matches")

@controller.get("/list-matches")
async def get_matches():
   matches_db = match_dao.list_matches()
   matches_view = match_db_to_view(matches_db)
   print(matches_view)
   return matches_view