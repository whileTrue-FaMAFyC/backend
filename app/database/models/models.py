from datetime import datetime
from os import getenv
from pony.orm import *

db = Database()


class User(db.Entity):
    user_id = PrimaryKey(int, auto=True, unsigned=True)
    username = Required(str, unique=True)
    email = Required(str, unique=True)
    avatar = Optional(str)
    hashed_password = Required(str)
    verification_code = Required(int, unsigned=True)
    verified = Required(bool)
    created_time = Required(datetime, default=lambda: datetime.now())
    robots = Set('Robot')
    matches_created = Set('Match')


class Robot(db.Entity):
    robot_id = PrimaryKey(int, auto=True, unsigned=True)
    name = Required(str)
    source_code = Required(str)
    owner = Required(User)
    avatar = Optional(str)
    matches_joined = Set('Match')
    match_results = Set('MatchResult')
    composite_key(name, owner)


class Match(db.Entity):
    match_id = PrimaryKey(int, auto=True, unsigned=True)
    name = Required(str)
    creator_user = Required(User)
    min_players = Required(int)
    max_players = Required(int)
    num_games = Required(int)
    num_rounds = Required(int)
    started = Required(bool)
    hashed_password = Optional(str)
    robots_joined = Set(Robot)
    match_results = Set('MatchResult')
    composite_key(name, creator_user)


class MatchResult(db.Entity):
    match_result_id = PrimaryKey(int, auto=True)
    robot = Required(Robot)
    match = Required(Match)
    games_won = Required(int, default=0)
    games_tied = Required(int, default=0)
    games_lost = Required(int, default=0)
    composite_key(robot, match)


def open_database(filename):
    db.bind('sqlite', filename, create_db=True)
    db.generate_mapping(create_tables=True)

# When testing (pytest), it gets set to TESTING and creates a database in
# RAM memory
RUNNING_ENVIRONMENT = getenv("DB_ENV", "DEPLOYMENT")
if RUNNING_ENVIRONMENT == "TESTING":
    open_database(':sharedmemory:')
else:
    open_database('database.sqlite')
