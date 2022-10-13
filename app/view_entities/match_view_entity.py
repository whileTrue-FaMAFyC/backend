from pydantic import BaseModel, validator
from pony.orm import db_session
from typing import List, Set
from database.models.models import Match

class UsernameView(BaseModel):
    username: str
    
    class Config:
        orm_mode = True
 
 
class RobotView(BaseModel):
    owner : UsernameView
    
    class Config:
        orm_mode = True

class MatchConfigView(BaseModel):
    name: str
    creator_user: UsernameView
    min_players: int
    max_players: int
    num_games: int
    num_rounds: int

    class Config:
        orm_mode = True

class ShowMatchView(BaseModel):
    config: MatchConfigView
    robots: List[RobotView]

@db_session
def match_db_to_view(matches: Match):
    robots_view = []
    matches_view = [MatchConfigView.from_orm(m) for m in matches]
    matches_and_robots = []

    for m in matches:
        robots_view.append([RobotView.from_orm(r) for r in m.robots_joined])

    for m in matches_view:
        for r in robots_view:
            matches_and_robots.append(ShowMatchView(config = m, robots = r))
    
    return matches_and_robots