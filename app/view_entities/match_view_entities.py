from pydantic import BaseModel

class NewMatch(BaseModel):
    name: str
    creator_robot: str
    min_players: int
    max_players: int
    num_games: int
    num_rounds: int
    password: str = ""

    class Config:
        orm_mode = True