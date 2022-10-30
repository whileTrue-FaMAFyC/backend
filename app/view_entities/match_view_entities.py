from pydantic import BaseModel
from typing import Dict

from view_entities import user_view_entities

# To add a new match to the database
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

# For listing matches
class MatchInfo(BaseModel):
    match_id: int
    name: str
    creator_user: user_view_entities.UserInMatch
    max_players: int

    class Config:
        orm_mode = True

# For listing matches with amount of robots joined
class ShowMatch(MatchInfo):
    robots_joined: int

# For showing the match details inside the lobby
class LobbyInfo(BaseModel):
    name: str
    creator_username: str
    min_players: int
    max_players: int
    num_games: int
    num_rounds: int
    users_joined: int
    user_robot: Dict[str, str]
    started: bool