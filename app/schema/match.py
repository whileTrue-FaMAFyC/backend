from fastapi import HTTPException
from typing import Union
from pydantic import BaseModel, validator, root_validator

class NewMatchSchema(BaseModel):
    name: str
    creator_user: str
    creator_robot: str
    min_players: int
    max_players: int
    num_games: int
    num_rounds: int
    password: Union[str, None] = None

    @validator('min_players')
    def min_players_req(min_players):
        if(min_players < 2 or min_players > 4):
            raise HTTPException(
                status_code=400,
                detail=f"Minimum amount of players can't be {min_players}"
            )
        return min_players

    @validator('max_players')
    def max_players_req(max_players):
        if(max_players < 2 or max_players > 4):
            raise HTTPException(
                status_code=400,
                detail=f"Maximum amount of players can't be {max_players}"
            )
        return max_players

    @root_validator
    def min_and_max(cls, values):
        if(values.get('min_players') > values.get('max_players')):
            raise HTTPException(
                status_code=400,
                detail=f"Minimum amount of players can't be greater than"
                        "maximum amount of players"
            )
        return values

    @validator('num_games')
    def num_games_req(num_games):
        if(num_games < 1 or num_games > 200):
            raise HTTPException(
                status_code=400,
                detail=f"Amount of games can't be {num_games}"
            )
        return num_games

    @validator('num_rounds')
    def num_rounds_req(num_rounds):
        if(num_rounds < 1 or num_rounds > 10000):
            raise HTTPException(
                status_code=400,
                detail=f"Amount of rounds can't be {num_rounds}"
            )
        return num_rounds

    class Config:
        orm_mode = True