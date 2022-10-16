from passlib.hash import bcrypt
from pony.orm import db_session, select

from database.dao import robot_dao
from database.models.models import Match, User 
from view_entities import match_view_entities

# The difference between creating a match for testing and creating an actual
# new match in the app is that in testing we try having more than one robot
# joined to the match, so we add these robots at creation. Creating an actual
# match would only add the creator's robot to it.
@db_session
def create_test_match(new_match: match_view_entities.MatchTest):
    creator = User.get(username=new_match.creator_user)

    set_robots = set()
    for r in new_match.robots_joined:
      set_robots.add(robot_dao.get_robot_by_name_and_user(r.name, r.owner.username))

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

@db_session
def get_match_by_name_and_user(match_name: str, creator_username: str):
    matches = Match.get(creator_user=User.get(username = creator_username), 
                        name=match_name)
    return matches

@db_session
def get_matches_by_username(username: str):
    matches = select(m.name for m in Match if m.creator_user.username == username)
    return matches

@db_session
def get_all_matches():
   matches = Match.select()
   return matches