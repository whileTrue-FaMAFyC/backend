from fastapi.testclient import TestClient
from fastapi import UploadFile
from pony.orm import db_session
from main import app
from database.dao import user_dao, robot_dao
from view_entities.user_view_entities import NewUserToDb
from view_entities.robot_view_entities import NewRobotView
import random
import string

# Usernames, robot names and match names used for the test
users = ['basbenja', 'jolcese', 'tonimond']
robots = [['robot1', 'robot2'], ['robot1', 'robot2'], ['robot1', 'robot2', 'robot3']]
matches = []
client = TestClient(app)

@db_session
def initial_users():
    users = [
        ('basbenja', 'basbenja@gmail.com', None, 'compu2317', '12345', True),
        ('jolcese', 'juliolcese@gmail.com', None, 'Whil3True', '56542', True),
        ('tonimond', 'tonimondejar@gmail.com', None, '122e31', '58924', False)
    ]
    for username, email, avatar, password, verif_code, verified in users:
        user_dao.create_user(NewUserToDb(username=username, email=email, avatar=avatar, 
                                         hashed_password=password, verification_code=verif_code, verified=verified))
    return

@db_session
def initial_robots():
    robots = [
        ('robot1',"basbenja@gmail.com", None, UploadFile(filename="A file read as UploadFile")),
        ('robot2',"basbenja@gmail.com", None, UploadFile(filename="Source code")),
        ('robot1',"juliolcese@gmail.com", None, UploadFile(filename="A file revfwrvrw {3428")),
        ('robot2',"juliolcese@gmail.com", None, UploadFile(filename="ciwd")),
        ('robot1',"tonimondejar@gmail.com", None, UploadFile(filename="cddddddddile")),
        ('robot2',"tonimondejar@gmail.com", None, UploadFile(filename="move")),
        ('robot3',"tonimondejar@gmail.com", None, UploadFile(filename="crgwe"))        
    ]
    for name, owner, avatar, source_code in robots:
        robot_dao.create_robot(NewRobotView(name=name, email=owner, avatar=avatar, source_code=source_code))
    return


def get_random_password():
    random_source = string.ascii_letters + string.digits + string.punctuation
    password = random.choice(string.ascii_lowercase)
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)
    length = random.randint(5, 100)

    for i in range(length):
        password += random.choice(random_source)

    password_list = list(password)
    random.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)
    return password

def get_random_match_name():
    password = ""
    random_source = string.ascii_letters + string.digits + string.punctuation
    length = random.randint(1, 30)

    for i in range(length):
        password += random.choice(random_source)

    password_list = list(password)
    random.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)
    return password

def client_put(match_name: str, creator_user: str, creator_robot: str,
               min_players: int, max_players: int, num_games: int,
               num_rounds: int, password: str):
    response = client.post(
        "/matches/new-match",
        json = {"name": match_name,
        "creator_user": creator_user,
        "creator_robot": creator_robot,
        "min_players": min_players,
        "max_players": max_players,
        "num_games": num_games,
        "num_rounds": num_rounds,
        "password": password
        }
    ) 
    return response

initial_users()
initial_robots()

def test_successful_creation():

    user_index = random.randint(0,2)
    creator_user = users[user_index]

    match_name = get_random_match_name()
    matches.append((creator_user,match_name))

    robot_index = random.randint(0, max(1,user_index))
    creator_robot = robots[user_index][robot_index]

    min_players = random.choice([2,3,4])

    max_players = random.randint(min_players, 4)

    num_games = random.randint(1, 200)

    num_rounds = random.randint(1, 10000)

    password = random.choice(["", get_random_password()])

    response = client_put(match_name, creator_user, creator_robot, min_players, 
                          max_players, num_games, num_rounds, password)

    assert response.status_code == 201
    return

@db_session
def test_invalid_robot():
    user_index = random.randint(0,2)
    creator_user = users[user_index]

    match_name = get_random_match_name()
    while((creator_user, match_name) in matches):
        match_name = get_random_match_name()
        
    creator_robot = 'unexistent robot'

    min_players = random.choice([2,3,4])

    max_players = random.randint(min_players, 4)

    num_games = random.randint(1, 200)

    num_rounds = random.randint(1, 10000)

    password = random.choice(["", get_random_password()])

    response = client_put(match_name, creator_user, creator_robot, min_players, 
                          max_players, num_games, num_rounds, password)

    assert response.status_code == 400
    assert response.json()["detail"] == f"Robot {creator_robot} isn't "\
                                        f"in {creator_user}'s library. "

    return

@db_session
def test_match_name_used():
    match_index = random.randint(0,len(matches)-1)
    match_name = matches[match_index][1]

    creator_user = matches[match_index][0]

    user_index = 0
    while(users[user_index] != creator_user):
        user_index = user_index + 1

    robot_index = random.randint(0, max(1,user_index))
    creator_robot = robots[user_index][robot_index]

    min_players = random.choice([2,3,4])

    max_players = random.randint(min_players, 4)

    num_games = random.randint(1, 200)

    num_rounds = random.randint(1, 10000)

    password = random.choice(["", get_random_password()])

    response = client_put(match_name, creator_user, creator_robot, min_players, 
                          max_players, num_games, num_rounds, password)

    assert response.status_code == 400
    assert response.json()["detail"] == f"{creator_user} already has a match "\
                                        f"named {match_name}. "

    return

@db_session
def test_invalid_min_players():

    user_index = random.randint(0,2)
    creator_user = users[user_index]

    match_name = get_random_match_name()
    while((creator_user, match_name) in matches):
        match_name = get_random_match_name()
        
    robot_index = random.randint(0, max(1,user_index))
    creator_robot = robots[user_index][robot_index]

    min_players = random.choice([random.randint(-100, 1), 
                                random.randint(5, 100)])

    max_players = random.randint(2, 4)

    num_games = random.randint(1, 200)

    num_rounds = random.randint(1, 10000)

    password = random.choice(["", get_random_password()])

    response = client_put(match_name, creator_user, creator_robot, min_players, 
                          max_players, num_games, num_rounds, password)

    # Here max_players will be between 2 and 4, but that could be a smaller
    # value than min_players, so the detail would include that.
    assert response.status_code == 400
    assert  ("Minimum amount of players has to be between 2 and 4." 
             in response.json()["detail"])

    return

@db_session
def test_invalid_max_players():

    user_index = random.randint(0,2)
    creator_user = users[user_index]

    match_name = get_random_match_name()
    while((creator_user, match_name) in matches):
        match_name = get_random_match_name()
        
    robot_index = random.randint(0, max(1,user_index))
    creator_robot = robots[user_index][robot_index]

    min_players = random.choice([2,3,4])

    max_players = random.choice([random.randint(-100, 1), 
                                 random.randint(5, 100)]) 
    num_games = random.randint(1, 200)

    num_rounds = random.randint(1, 10000)

    password = random.choice(["", get_random_password()])

    print(max_players)
    response = client_put(match_name, creator_user, creator_robot, min_players, 
                          max_players, num_games, num_rounds, password)

    assert response.status_code == 400
    assert ("Maximum amount of players has to be between 2 and 4. " 
            in response.json()["detail"])
    return

@db_session
def test_min_greater_than_max():

    user_index = random.randint(0,2)
    creator_user = users[user_index]

    match_name = get_random_match_name()
    while((creator_user, match_name) in matches):
        match_name = get_random_match_name()
        
    robot_index = random.randint(0, max(1,user_index))
    creator_robot = robots[user_index][robot_index]

    min_players = random.randint(3, 4)

    max_players = random.randint(2, min_players-1)

    num_games = random.randint(1, 200)

    num_rounds = random.randint(1, 10000)

    password = random.choice(["", get_random_password()])

    response = client_put(match_name, creator_user, creator_robot, min_players, 
                          max_players, num_games, num_rounds, password)

    assert response.status_code == 400
    assert response.json()["detail"] == "Minimum amount of players can't be " \
                                        "greater than maximum amount of " \
                                        "players. "

    return

@db_session
def test_invalid_games():

    user_index = random.randint(0,2)
    creator_user = users[user_index]

    match_name = get_random_match_name()
    while((creator_user, match_name) in matches):
        match_name = get_random_match_name()
        
    robot_index = random.randint(0, max(1,user_index))
    creator_robot = robots[user_index][robot_index]

    min_players = random.choice([2,3,4])

    max_players = random.randint(min_players, 4)

    num_games = random.choice([random.randint(-100, 0), 
                               random.randint(200, 300)])

    num_rounds = random.randint(1, 100000)

    password = random.choice(["", get_random_password()])

    response = client_put(match_name, creator_user, creator_robot, min_players, 
                          max_players, num_games, num_rounds, password)

    assert response.status_code == 400
    assert response.json()["detail"] == "Number of games has to be between "\
                                        "1 and 200. "

    return

@db_session
def test_invalid_rounds():

    user_index = random.randint(0,2)
    creator_user = users[user_index]

    match_name = get_random_match_name()
    while((creator_user, match_name) in matches):
        match_name = get_random_match_name()
        
    robot_index = random.randint(0, max(1,user_index))
    creator_robot = robots[user_index][robot_index]

    min_players = random.choice([2,3,4])

    max_players = random.randint(min_players, 4)

    num_games = random.randint(1, 200)

    num_rounds = random.choice([random.randint(-100, 0), 
                                random.randint(100001, 100101)])

    password = random.choice(["", get_random_password()])

    response = client_put(match_name, creator_user, creator_robot, min_players, 
                          max_players, num_games, num_rounds, password)

    assert response.status_code == 400
    assert response.json()["detail"] == "Number of rounds has to be between "\
                                        "1 and 100000. "

    return