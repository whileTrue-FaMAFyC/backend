from pydantic import BaseModel
from typing import List

from view_entities.user_view_entities import UserInMatch
from view_entities.robot_view_entities import WinnerRobot, RobotPlayer

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
    creator_user: UserInMatch
    max_players: int

    class Config:
        orm_mode = True

# For listing matches with amount of robots joined
class ShowMatch(MatchInfo):
    robots_joined: int

class StartMatch(BaseModel):
    num_games: int
    num_rounds: int
    robots_joined: List[RobotPlayer]

class StartMatchValidator(BaseModel):
    creator_username: str
    min_players: int
    started: bool
    robots_joined: int

#For showing the competitor(user and his robot) details inside the lobby.
class UserAndRobotInfo(BaseModel):
    username: str
    user_avatar: str
    robot_name: str
    robot_avatar: str

class JoinMatch(BaseModel):
    match_password: str = ""
    joining_robot: str
    
# For showing the match details inside the lobby
class LobbyInfo(BaseModel):
    requester_username: str
    name: str
    creator_username: str
    min_players: int
    max_players: int
    num_games: int
    num_rounds: int
    users_joined: int
    user_robot: List[UserAndRobotInfo]
    started: bool
    im_in: bool
    is_creator: bool
    results: List[WinnerRobot]
    has_password: bool


class JoinMatch(BaseModel):
    match_password: str = ""
    joining_robot: str