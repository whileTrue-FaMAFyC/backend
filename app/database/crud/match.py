from pony.orm import db_session
from database.models import Match, User, Robot
from schema import match

@db_session
def add_new_match(new_match: match.NewMatchSchema):
    creator = User.get(username=new_match.creator_user)
    robot_creator = Robot.get(name=new_match.creator_robot, owner=creator)
    db_match = Match(
        name = new_match.name,
        creator_user = creator,
        robots_joined = [robot_creator],
        min_players = new_match.min_players,
        max_players = new_match.max_players,
        num_games = new_match.num_games,
        num_rounds = new_match.num_rounds,
        started = False,
        password = new_match.password
    )
# Falta encriptar password

@db_session
def is_name_available(match_name: str, creator_name: str):
    matches = Match.get(creator_user = User.get(username=creator_name), name = match_name)
    return matches