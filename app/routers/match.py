from fastapi import HTTPException, APIRouter
from schema.match import NewMatchSchema
from database.crud import match, robot

router = APIRouter(prefix="/matches")

@router.post("/new-match")
async def create_match(new_match: NewMatchSchema):
    users_robot = robot.belongs_to_user(new_match.creator_robot, 
                                         new_match.creator_user)
    name_in_use = match.is_name_available(new_match.name, 
                                         new_match.creator_user)
    if not(users_robot):
        raise HTTPException(
            status_code=400,
            detail=f"Robot {new_match.creator_robot} isn't in {new_match.creator_user}'s library")
    if name_in_use:
        raise HTTPException(
            status_code=400,
            detail=f"{new_match.creator_user} already has a match named {new_match.name}")

    new_db_match = match.add_new_match(new_match)
    return new_db_match