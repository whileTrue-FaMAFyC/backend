from pydantic import BaseModel

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

class JoinMatch(BaseModel):
    match_id: int
    match_password: str = ""
    joining_robot: str

class JoinMatchBroadcast(BaseModel):
    action: str
    data: user_view_entities.JoinMatchUser