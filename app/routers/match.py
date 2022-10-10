from fastapi import HTTPException, APIRouter, status
from schema.match import NewMatchSchema
from database.crud import match, robot

router = APIRouter(prefix="/matches")

@router.post("/new-match", status_code = status.HTTP_201_CREATED)
async def create_match(new_match: NewMatchSchema):
    users_robot = robot.belongs_to_user(new_match.creator_robot, 
                                         new_match.creator_user)
    name_in_use = match.is_name_available(new_match.name, 
                                         new_match.creator_user)
    if not(users_robot):
        raise HTTPException(
            status_code=400,
            detail=f"Robot {new_match.creator_robot} isn't in"
                   f"{new_match.creator_user}'s library")
    if name_in_use:
        raise HTTPException(
            status_code=400,
            detail=f"{new_match.creator_user} already has a match"
                   f"named {new_match.name}")

    match.add_new_match(new_match)
    return