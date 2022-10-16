from pydantic import BaseModel
from typing import Union

class NewMatch(BaseModel):
    name: str
#    creator_user: str
    creator_robot: str
    min_players: int
    max_players: int
    num_games: int
    num_rounds: int
    password: Union[str, None] = None

    class Config:
        orm_mode = True