from pony.orm import *

db = Database()

class User(db.Entity):
    user_id = PrimaryKey(int, auto=True, unsigned=True)
    username = Required(str, 20, unique=True)
    email = Required(str, 50, unique=True)
    avatar = Optional(buffer)
    hashed_password = Required(str)
    verification_code = Required(int, unsigned=True)
    verified = Required(bool)
    robots = Set('Robot')
    matches_created = Set('Match')


class Robot(db.Entity):
    robot_id = PrimaryKey(int, auto=True, unsigned=True)
    name = Required(str)
    source_code = Required(str)
    owner = Required(User)
    avatar = Optional(buffer)
    matches_joined = Set('Match')
    composite_key(name, owner)


class Match(db.Entity):
    match_id = PrimaryKey(int, auto=True, unsigned=True)
    name = Required(str, 30)
    creator_user = Required(User)
    min_players = Required(int)
    max_players = Required(int)
    num_games = Required(int)
    num_rounds = Required(int)
    started = Required(bool)
    hashed_password = Optional(str)
    robots_joined = Set(Robot)
    composite_key(name, creator_user)

def bind_database(filename: str):
    db.bind('sqlite', filename, create_db=True)
    db.generate_mapping(create_tables=True)

RUNNING_ENVIRONMENT = getenv("DB_ENV", "APP_DB")

if RUNNING_ENVIRONMENT == "TESTING":
    bind_database(':sharedmemory:')
else:
    bind_database('database_pyrobots.sqlite')