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


class ShowStats(BaseModel):
    matches_played: int
    matches_won: int
    matches_tied: int
    matches_lost: int
    games_win_rate: int

    class Config:
        orm_mode = True


class ShowRobot(BaseModel):
    name: str
    avatar: str
    stats: ShowStats

    class Config:
        orm_mode = True


class RobotPlayer(BaseModel):
    name: str
    robot_id: int

    class Config:
        orm_mode = True


class WinnerRobot(BaseModel):
    username: str
    robot_name: str

class RobotInSimulation(BaseModel):
    name: str
    id: int