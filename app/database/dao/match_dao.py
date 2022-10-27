from passlib.hash import bcrypt
from pony.orm import db_session, select

from database.models.models import Match, Robot, User 
from utils.robot_utils import get_robot_in_match
from view_entities.match_view_entities import NewMatch, AbandonMatch

@db_session
def create_new_match(creator_username, new_match: NewMatch):
    creator = User.get(username=creator_username)
    robot_creator = Robot.get(name=new_match.creator_robot, owner=creator)
    
    if (new_match.password):
        match_password = bcrypt.hash(new_match.password)
    else: # The match doesn't have a password
        match_password = ""
    try:
        Match(
            name=new_match.name,
            creator_user=creator,
            robots_joined=[robot_creator],
            min_players=new_match.min_players,
            max_players=new_match.max_players,
            num_games=new_match.num_games,
            num_rounds=new_match.num_rounds,
            started=False,
            hashed_password=match_password
        )
        return True
    except:
        return False

@db_session
def get_match_by_name_and_user(match_name: str, creator_username: str):
    matches = Match.get(creator_user=User.get(username=creator_username), 
                        name=match_name)
    return matches

@db_session
def get_all_matches():
    matches = Match.select()
    return matches

@db_session
def select_robots_from_match(match_name: str, creator_username: str):
    
    return select(m.robots_joined for m in Match
                  if m.creator_user == User.get(username=creator_username)
                  and m.name == match_name)

@db_session
def update_abandoning_user(abandoning_user: str, match_info: AbandonMatch):
    
    match = Match.get(name=match_info.name, 
                      creator_user=User.get(username=match_info.creator_user))

    robot = get_robot_in_match(match_info, abandoning_user)
    
    try:
        match.robots_joined.remove(robot)
        return True
    except:
        return False