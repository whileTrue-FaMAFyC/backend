from pydantic import BaseModel
from typing import Union
from view_entities import user_view_entities

class RobotInMatch(BaseModel):
    owner : user_view_entities.UserInMatch
    name : str

    class Config:
        orm_mode = True

class NewRobot(BaseModel):
    name: str
    email: str
    avatar: Union[str, None] = None
    source_code: str