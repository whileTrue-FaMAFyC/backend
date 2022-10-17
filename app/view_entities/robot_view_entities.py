from pydantic import BaseModel

from view_entities import user_view_entities

class RobotInMatch(BaseModel):
    owner: user_view_entities.UserInMatch
    name: str

    class Config:
        orm_mode = True