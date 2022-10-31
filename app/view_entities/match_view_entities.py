from pydantic import BaseModel
from typing import List

from view_entities import robot_view_entities, user_view_entities

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

class MatchInfo(BaseModel):
    match_id: int
    name: str
    creator_user: user_view_entities.UserInMatch
    max_players: int

    class Config:
        orm_mode = True

class ShowMatch(MatchInfo):
    robots_joined: int

class StartMatch(BaseModel):
    num_games: int
    num_rounds: int
    robots_joined: List[robot_view_entities.RobotPlayer]

class StartMatchValidator(BaseModel):
    creator_username: str
    min_players: int
    started: bool
    robots_joined: int