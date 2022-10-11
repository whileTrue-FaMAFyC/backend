from fastapi import APIRouter
from database.crud import match

match_router = APIRouter(prefix="/matches")

@match_router.get("/list-matches")
async def get_matches():
   matches = match.list_matches()
   return matches
