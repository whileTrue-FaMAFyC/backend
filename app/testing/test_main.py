from fastapi.testclient import TestClient
from fastapi import UploadFile
from pony.orm import db_session
from database.dao import match_dao
from main import app
from database.dao import user_dao, robot_dao, match_dao
from view_entities.user_view_entities import NewUserToDb, UserInMatchView
from view_entities.robot_view_entities import NewRobotView, RobotInMatchView
from view_entities.match_view_entities import TMatchView
from response import possible_responses

# Usernames, robot names and match names used for the test
client = TestClient(app)

@db_session
def initial_users():
    users = [
        ('basbenja', 'basbenja@gmail.com', None, 'compu2317', '12345', True),
        ('jolcese', 'juliolcese@gmail.com', None, 'Whil3True', '56542', True),
        ('tonimond', 'tonimondejar@gmail.com', None, '122e31', '58924', False)
    ]
    for username, email, avatar, password, verif_code, verified in users:
        user_dao.create_user(NewUserToDb(
                             username=username, email=email, avatar=avatar, 
                             hashed_password=password, 
                             verification_code=verif_code, verified=verified))
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

@db_session
def initial_matches():
    matches = [
        ('match1', 'basbenja', 'robot1', 2, 4, 10, 1570, "", 
        [RobotInMatchView(owner=UserInMatchView(username="basbenja"), name="robot1"), RobotInMatchView(owner=UserInMatchView(username="jolcese"), name="robot1")]),
        ('match2', 'basbenja', 'robot2', 3, 3, 200, 100000, "matchPass!", [RobotInMatchView(owner=UserInMatchView(username="basbenja"), name="robot2")]),
        ('match1', 'jolcese', 'robot1', 2, 3, 1, 1, "P455W0RD", [RobotInMatchView(owner=UserInMatchView(username="jolcese"), name="robot1")]),
        ('jmatch2', 'jolcese', 'robot1', 2, 3, 1, 1, "P455W0RD", [RobotInMatchView(owner=UserInMatchView(username="jolcese"), name="robot1")]),
        ('24601', 'tonimond', 'robot1', 2, 2, 157, 3250, "", [RobotInMatchView(owner=UserInMatchView(username="tonimond"), name="robot1")]),
        ('match!', 'tonimond', 'robot3', 4, 4, 200, 1, "pw", 
         [RobotInMatchView(owner=UserInMatchView(username="tonimond"), name="robot3"), RobotInMatchView(owner=UserInMatchView(username="basbenja"), name="robot2"), RobotInMatchView(owner=UserInMatchView(username="jolcese"), name="robot1")])
    ]
    for (name, creator_user, creator_robot, min_players, max_players, 
         num_games, num_rounds, password, robots_joined) in matches:
        print(robots_joined)
        match_dao.create_test_match(
            TMatchView(name=name, creator_user=creator_user,
                          creator_robot=creator_robot, min_players=min_players,
                          max_players=max_players, num_games=num_games, 
                          num_rounds=num_rounds, password=password, 
                          robots_joined=robots_joined))
    return

def test_no_matches():
    response = client.get(
        "/matches/list-matches"
    )
    assert response.status_code == 200
    assert response.json() == []
    return


def test_with_matches():
    initial_users()
    initial_robots()
    initial_matches()

    response = client.get(
        "/matches/list-matches"
    )
    assert response.status_code == 200
    print(response.json())
    assert response.json() in possible_responses