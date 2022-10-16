from database.models.models import Match, Robot, User 
from passlib.context import CryptContext
from pony.orm import db_session, select
from view_entities import match_view_entities

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Creation
@db_session
def create_new_match(creator_username, new_match: match_view_entities.NewMatch):
    creator = User.get(username=creator_username)
    robot_creator = Robot.get(name=new_match.creator_robot, owner=creator)
    
    if(new_match.password):
        match_password = pwd_context.hash(new_match.password)
    else: # The match doesn't have a password
        match_password = ""
    try:
        Match(
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
        return True
    except:
        return False

# Queries
@db_session
def get_match_by_name_and_user(match_name: str, creator_username: str):
    matches = Match.get(creator_user = User.get(username=creator_username), 
                        name = match_name)
    return matches

@db_session
def get_matches_by_username(username: str):
    matches = select(m.name for m in Match if m.creator_user.username == username)
    return matches

@db_session
def get_all_matches():
    matches = Match.select()
    return matches