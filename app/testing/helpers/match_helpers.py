from pony.orm import db_session
from passlib.hash import bcrypt
from pydantic import BaseModel
from typing import List

from database.dao.robot_dao import get_robot_by_name_and_user
from database.models.models import User, Match
from view_entities.robot_view_entities import RobotInMatch

class MatchTest(BaseModel):
    name: str
    creator_user: str
    creator_robot: str
    min_players: int
    max_players: int
    num_games: int
    num_rounds: int
    password: str = ""
    robots_joined: List[RobotInMatch]

    class Config:
        orm_mode = True

# The difference between creating a match for testing and creating an actual
# new match in the app is that in testing we try having more than one robot
# joined to the match, so we add these robots at creation. Creating an actual
# match would only add the creator's robot to it.
@db_session
def create_test_match(new_match: MatchTest):
    creator = User.get(username=new_match.creator_user)

    set_robots = set()
    for r in new_match.robots_joined:
      set_robots.add(get_robot_by_name_and_user(r.name, r.owner.username))

    if(new_match.password):
        match_password = bcrypt.hash(new_match.password)
    else:
        match_password = new_match.password

    db_match = Match(
        name=new_match.name,
        creator_user=creator,
        min_players=new_match.min_players,
        max_players=new_match.max_players,
        num_games=new_match.num_games,
        num_rounds=new_match.num_rounds,
        started=False,
        hashed_password=match_password,
        robots_joined=set_robots
    )

    return db_match