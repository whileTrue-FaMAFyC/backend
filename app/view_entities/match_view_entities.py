from pydantic import BaseModel
from typing import List, Union
from view_entities import robot_view_entities, user_view_entities

class MatchConfigView(BaseModel):
    name: str
    creator_user: user_view_entities.UserInMatchView
    min_players: int
    max_players: int
    num_games: int
    num_rounds: int

    class Config:
        orm_mode = True

class ShowMatchView(BaseModel):
    config: MatchConfigView
    robots: List[robot_view_entities.RobotInMatchView]

class TMatchView(BaseModel):
    name: str
    creator_user: str
    creator_robot: str
    min_players: int
    max_players: int
    num_games: int
    num_rounds: int
    password: Union[str, None] = None
    robots_joined: List[robot_view_entities.RobotInMatchView]

    class Config:
        orm_mode = True