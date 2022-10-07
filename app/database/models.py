from pony.orm import *


db = Database()


class User(db.Entity):
    username = PrimaryKey(str, auto=True)
    email = Required(str, unique=True)
    avatar = Optional(buffer)
    password = Required(str)
    verificationCode = Required(int)
    verified = Required(bool)
    robots = Set('Robot')
    matchsCreated = Set('Match', reverse='creatorUser')
    matchsJoined = Set('Match', reverse='usersJoined')


class Robot(db.Entity):
    name = Required(str)
    owner = Required(User)
    avatar = Optional(buffer)
    matchsJoined = Set('Match')
    PrimaryKey(name, owner)


class Match(db.Entity):
    name = Required(str)
    creatorUser = Required(User, reverse='matchsCreated')
    usersJoined = Set(User, reverse='matchsJoined')
    robotsJoined = Set(Robot)
    minPlayers = Required(int)
    maxPlayers = Required(int)
    numGames = Required(int)
    numRounds = Required(int)
    started = Required(bool)
    PrimaryKey(name, creatorUser)



db.generate_mapping()