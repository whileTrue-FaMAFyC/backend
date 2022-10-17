from pydantic import BaseModel

from view_entities.user_view_entities import UserInMatch

class BotCreate(BaseModel):
    name: str
    source_code: str
    bot_filename: str
    avatar: str = ""

class RobotInMatch(BaseModel):
    owner: UserInMatch
    name: str

    class Config:
        orm_mode = True