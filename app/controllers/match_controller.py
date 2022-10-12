from database.dao import match_dao
from fastapi import APIRouter, status
from validators.match_validators import new_match_val
from view_entities.match_view_entity import NewMatchView

controller = APIRouter(prefix="/matches")

@controller.post("/new-match", status_code = status.HTTP_201_CREATED)
async def create_match(new_match: NewMatchView):
    new_match_val(new_match)
    match_dao.add_new_match(new_match)
    return