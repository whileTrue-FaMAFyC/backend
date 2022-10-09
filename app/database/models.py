from pony.orm import *


db = Database()


class User(db.Entity):
    username = Required(str)
    email = PrimaryKey(str)
    avatar = Optional(buffer)
    password = Required(str)
    verification_code = Required(int)
    verified = Required(bool)
    robots = Set('Robot')
    matches_created = Set('Match')


class Robot(db.Entity):
    name = Required(str)
    owner = Required(User)
    avatar = Optional(buffer)
    matches_joined = Set('Match')
    source_code = Required(buffer)
    PrimaryKey(name, owner)


class Match(db.Entity):
    name = Required(str)
    creator_user = Required(User)
    robots_joined = Set(Robot)
    min_players = Required(int)
    max_players = Required(int)
    num_games = Required(int)
    num_rounds = Required(int)
    started = Required(bool)
    password = Optional(str)
    PrimaryKey(name, creator_user)

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)

db.generate_mapping(create_tables=True)
