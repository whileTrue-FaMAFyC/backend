from pydantic import BaseModel
from typing import List

from view_entities import robot_view_entities, user_view_entities

class MatchInfo(BaseModel):
    match_id: int
    name: str
    creator_user: user_view_entities.UserInMatch
    max_players: int

    class Config:
        orm_mode = True

class ShowMatch(MatchInfo):
    robots_joined: int

class MatchTest(BaseModel):
    name: str
    creator_user: str
    creator_robot: str
    min_players: int
    max_players: int
    num_games: int
    num_rounds: int
    password: str = ""
    robots_joined: List[robot_view_entities.RobotInMatch]

    class Config:
        orm_mode = True