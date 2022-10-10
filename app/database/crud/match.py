from pony.orm import db_session
from database.models import Match, User, Robot
from schema import match
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@db_session
def add_new_match(new_match: match.NewMatchSchema):
    creator = User.get(username=new_match.creator_user)
    robot_creator = Robot.get(name=new_match.creator_robot, owner=creator)
    if(new_match.password):
        match_password = pwd_context.hash(new_match.password)
    else:
        match_password = new_match.password

    db_match = Match(
        name = new_match.name,
        creator_user = creator,
        robots_joined = [robot_creator],
        min_players = new_match.min_players,
        max_players = new_match.max_players,
        num_games = new_match.num_games,
        num_rounds = new_match.num_rounds,
        started = False,
        hashed_password = match_password
    )
    return new_match.name

@db_session
# Returns True if the user with username `creator_username` hasn't created
# a match with name `match_name` yet. False otherwise. 
def is_name_available(match_name: str, creator_username: str):
    matches = Match.get(creator_user = User.get(username=creator_username), 
                        name = match_name)
    return matches