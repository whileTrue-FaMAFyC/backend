from fastapi import UploadFile
from pydantic import BaseModel
from typing import Union
from view_entities import user_view_entities

class RobotInMatchView(BaseModel):
    owner : user_view_entities.UserInMatchView
    name : str

    class Config:
        orm_mode = True

class NewRobotView(BaseModel):
    name: str
    email: str
    avatar: Union[UploadFile, None] = None
    source_code: UploadFile