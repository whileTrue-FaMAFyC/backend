from database.dao import user_dao, robot_dao, match_dao
from fastapi.testclient import TestClient
from generate_token import MOCK_TOKEN_BENJA
from main import app
from pony.orm import db_session
from view_entities.match_view_entities import MatchTest
from view_entities.user_view_entities import NewUserToDb, UserInMatch
from view_entities.robot_view_entities import NewRobot, RobotInMatch

client = TestClient(app)

MOCK_SOURCE_CODE = """aW1wb3J0IHV2aWNvcm4KCgppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgog
                      ICAgdXZpY29ybi5ydW4oImFwcC5hcGk6YXBwIiwgaG9zdD0iMC4wLjAuMCIs
                      IHBvcnQ9ODAwMCwgcmVsb2FkPVRydWUp"""

MOCK_AVATAR = """iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQ
                 DwAEhQGAhKmMIQAAAABJRU5ErkJggg=="""

# Mock users used for the test.
@db_session
def initial_users():
    users = [
        ('basbenja', 'basbenja@gmail.com', MOCK_AVATAR, 'compu2317', '12345', True),
        ('jolcese', 'juliolcese@gmail.com', MOCK_AVATAR, 'Whil3True', '56542', True),
        ('tonimond', 'tonimondejar@gmail.com', MOCK_AVATAR, '122e31', '58924', True)
    ]

    for username, email, avatar, password, verif_code, verified in users:
        user_dao.create_user(NewUserToDb(username = username, email = email, 
                             avatar = avatar, hashed_password = password, 
                             verification_code = verif_code, verified = verified))
    return

# Mock robots used for the test.
@db_session
def initial_robots():
    robots = [
        ('robot1',"basbenja@gmail.com", MOCK_AVATAR, MOCK_SOURCE_CODE),
        ('robot2',"basbenja@gmail.com", MOCK_AVATAR, MOCK_SOURCE_CODE),
        ('robot1',"juliolcese@gmail.com", MOCK_AVATAR, MOCK_SOURCE_CODE),
        ('robot2',"juliolcese@gmail.com", MOCK_AVATAR, MOCK_SOURCE_CODE),
        ('robot1',"tonimondejar@gmail.com", MOCK_AVATAR, MOCK_SOURCE_CODE),
        ('robot2',"tonimondejar@gmail.com", MOCK_AVATAR, MOCK_SOURCE_CODE),
        ('robot3',"tonimondejar@gmail.com", MOCK_AVATAR, MOCK_SOURCE_CODE)        
    ]

    for name, owner, avatar, source_code in robots:
        robot_dao.create_robot(NewRobot(name=name, email=owner, 
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
         RobotInMatch(owner=UserInMatch(username="jolcese"), name="robot1")])
    ]

    for (name, creator_user, creator_robot, min_players, max_players, 
         num_games, num_rounds, password, robots_joined) in matches:
        match_dao.create_test_match(
            MatchTest(name = name, creator_user = creator_user,
                      creator_robot = creator_robot, min_players = min_players,
                      max_players = max_players, num_games = num_games, 
                      num_rounds = num_rounds, password = password, 
                      robots_joined = robots_joined))
    return


# Test case where there are no matches created.
def test_no_matches():
    response = client.get("/matches/list-matches",
                          headers = {"Authorization": MOCK_TOKEN_BENJA})
    assert response.status_code == 200
    assert response.json() == []
    return

expected_response =  [
  {"match_id": 1, "name": "match1", "creator_user": {"username": "basbenja"}, 
  "max_players": 4, "robots_joined": 2}, 
  {"match_id": 2, "name": "match2", "creator_user": {"username": "basbenja"}, 
  "max_players": 3, "robots_joined": 1},
  {"match_id": 3, "name": "match1", "creator_user": {"username": "jolcese"}, 
  "max_players": 3, "robots_joined": 1},
  {"match_id": 4, "name": "jmatch2", "creator_user": {"username": "jolcese"}, 
  "max_players": 3, "robots_joined": 1},
  {"match_id": 5, "name": "24601", "creator_user": {"username": "tonimond"}, 
  "max_players": 2, "robots_joined": 1},
  {"match_id": 6, "name": "match!", "creator_user": {"username": "tonimond"}, 
  "max_players": 4, "robots_joined": 3}]

# In this test we first create new matches and then analyze the behavior.
def test_with_matches():
    # To create a match, we first need users and robots stored in the database,
    # that's why we mocked them as well.
    initial_users()
    initial_robots()
    initial_matches()

    response = client.get("/matches/list-matches",
                          headers = {"Authorization": MOCK_TOKEN_BENJA})

    assert response.status_code == 200
    assert response.json() == expected_response