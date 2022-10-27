from fastapi.testclient import TestClient
from pony.orm import db_session

from database.dao import user_dao
from database.models.models import db
from main import app
from testing.helpers.generate_token import MOCK_TOKEN_BENJA, MOCK_TOKEN_JULI_J, MOCK_TOKEN_TONI
from testing.helpers.robot_helpers import NewRobot, create_robot
from testing.helpers.match_helpers import MatchTest, create_test_match
from utils.user_utils import INVALID_TOKEN_EXCEPTION
from utils.match_utils import INEXISTENT_MATCH_EXCEPTION, USER_NOT_JOINED_EXCEPTION
from view_entities.user_view_entities import NewUserToDb, UserInMatch
from view_entities.robot_view_entities import RobotInMatch


# Usernames, robot names and match names used for the test
tokens = [MOCK_TOKEN_BENJA, MOCK_TOKEN_JULI_J, MOCK_TOKEN_TONI]
users = ['basbenja', 'jolcese', 'tonimond']
robots = [['robot1', 'robot2'], ['robot1', 'robot2'], ['robot1', 'robot2', 'robot3']]
matches = []
MOCK_SOURCE_CODE = """aW1wb3J0IHV2aWNvcm4KCgppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgog
                      ICAgdXZpY29ybi5ydW4oImFwcC5hcGk6YXBwIiwgaG9zdD0iMC4wLjAuMCIs
                      IHBvcnQ9ODAwMCwgcmVsb2FkPVRydWUp"""
MOCK_AVATAR = """iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQ
                 DwAEhQGAhKmMIQAAAABJRU5ErkJggg=="""

client = TestClient(app)

@db_session
def initial_users():
    users = [
        ('basbenja', 'basbenja@gmail.com', MOCK_AVATAR, 'compu2317', '12345', True),
        ('jolcese', 'juliolcese@gmail.com', "", 'Whil3True', '56542', True),
        ('tonimond', 'tonimondejar@gmail.com', MOCK_AVATAR, '122e31', '58924', True)
    ]
    for username, email, avatar, password, verif_code, verified in users:
        user_dao.create_user(NewUserToDb(username=username, email=email, 
                                         avatar=avatar, hashed_password=password, 
                                         verification_code=verif_code, 
                                         verified=verified))
    return

@db_session
def initial_robots():
    robots = [
        ('robot1',"basbenja@gmail.com", "", MOCK_SOURCE_CODE),
        ('robot2',"basbenja@gmail.com", MOCK_AVATAR, MOCK_SOURCE_CODE),
        ('robot1',"juliolcese@gmail.com", MOCK_AVATAR, MOCK_SOURCE_CODE),
        ('robot2',"juliolcese@gmail.com", "", MOCK_SOURCE_CODE),
        ('robot1',"tonimondejar@gmail.com", MOCK_AVATAR, MOCK_SOURCE_CODE),
        ('robot2',"tonimondejar@gmail.com", MOCK_AVATAR, MOCK_SOURCE_CODE),
        ('robot3',"tonimondejar@gmail.com", MOCK_AVATAR, MOCK_SOURCE_CODE)        
    ]
    for name, owner, avatar, source_code in robots:
        create_robot(NewRobot(name=name, email=owner, 
                            avatar=avatar, source_code=source_code))
    return

# Mock matches used for the test.
@db_session
def initial_matches():
    matches = [
        ('match1', 'basbenja', 'robot1', 2, 4, 10, 1570, "", 
        [RobotInMatch(owner=UserInMatch(username="basbenja"), name="robot1"), 
         RobotInMatch(owner=UserInMatch(username="jolcese"), name="robot1")]),
        ('match2', 'basbenja', 'robot2', 3, 3, 200, 100000, "matchPass!", 
        [RobotInMatch(owner=UserInMatch(username="basbenja"), name="robot2")]),
        ('match1', 'jolcese', 'robot1', 2, 3, 1, 1, "P455W0RD", 
        [RobotInMatch(owner=UserInMatch(username="jolcese"), name="robot1")]),
        ('jmatch2', 'jolcese', 'robot1', 2, 3, 1, 1, "P455W0RD", 
        [RobotInMatch(owner=UserInMatch(username="jolcese"), name="robot1")]),
        ('24601', 'tonimond', 'robot1', 2, 2, 157, 3250, "", 
        [RobotInMatch(owner=UserInMatch(username="tonimond"), name="robot1")]),
        ('match!', 'tonimond', 'robot3', 4, 4, 200, 1, "pw", 
         [RobotInMatch(owner=UserInMatch(username="tonimond"), name="robot3"), 
         RobotInMatch(owner=UserInMatch(username="basbenja"), name="robot2"), 
         RobotInMatch(owner=UserInMatch(username="jolcese"), name="robot2")])
    ]

    for (name, creator_user, creator_robot, min_players, max_players, 
         num_games, num_rounds, password, robots_joined) in matches:
        create_test_match(
            MatchTest(name=name, creator_user=creator_user,
                      creator_robot=creator_robot, min_players=min_players,
                      max_players=max_players, num_games=num_games, 
                      num_rounds=num_rounds, password=password, 
                      robots_joined=robots_joined))
    return

def test_inexistent_match():
    db.drop_all_tables(with_all_data=True)
    db.create_tables()
    initial_users()
    initial_robots()
    initial_matches()

    response = client.delete("/matches/abandon-match",
                          headers = {"Authorization": MOCK_TOKEN_BENJA},
                          json = {"creator_user": "tonimond",
                                  "name": "inexistent"})

    assert response.status_code == INEXISTENT_MATCH_EXCEPTION.status_code
    assert response.json()["detail"] == INEXISTENT_MATCH_EXCEPTION.detail
    return

def test_user_not_joined():
    response = client.delete("/matches/abandon-match",
                          headers = {"Authorization": MOCK_TOKEN_BENJA},
                          json = {"creator_user": "jolcese",
                                  "name": "jmatch2"})

    assert response.status_code == USER_NOT_JOINED_EXCEPTION.status_code
    assert response.json()["detail"] == USER_NOT_JOINED_EXCEPTION.detail
    return


def test_successful_abandonment():
    response = client.delete("/matches/abandon-match",
                          headers = {"Authorization": MOCK_TOKEN_BENJA},
                          json = {"creator_user": "tonimond",
                                  "name": "match!"})

    assert response.status_code == 200
    return

def test_invalid_token():
    response = client.delete("/matches/abandon-match",
                          headers = {"Authorization": "abc"},
                          json = {"creator_user": "tonimond",
                                  "name": "match!"})
    
    assert response.status_code == INVALID_TOKEN_EXCEPTION.status_code
    assert response.json()["detail"] == INVALID_TOKEN_EXCEPTION.detail