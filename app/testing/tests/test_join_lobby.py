from fastapi.testclient import TestClient
from pony.orm import db_session

from main import app
from database.dao import user_dao
from database.dao.match_dao import get_match_by_name_and_user
from database.models.models import db
from testing.helpers.generate_token import MOCK_TOKEN_BENJA
from testing.helpers.robot_helpers import NewRobot, create_robot
from testing.helpers.match_helpers import MatchTest, create_test_match
from view_entities.user_view_entities import NewUserToDb, UserInMatch
from view_entities.robot_view_entities import RobotInMatch


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
        ('basbenja', 'basbenja@gmail.com', '', 'compu2317', '12345', True),
        ('jolcese', 'juliolcese@gmail.com', MOCK_AVATAR, 'Whil3True', '56542', True),
        ('tonimond', 'tonimondejar@gmail.com', MOCK_AVATAR, '122e31', '58924', True)
    ]

    for username, email, avatar, password, verif_code, verified in users:
        user_dao.create_user(
            NewUserToDb(
                username=username, 
                email=email, 
                avatar=avatar, hashed_password=password, 
                verification_code=verif_code, verified=verified
            )
        )
    return

# Mock robots used for the test.
@db_session
def initial_robots():
    robots = [
        ('robot1',"basbenja@gmail.com", MOCK_AVATAR, MOCK_SOURCE_CODE),
        ('robot2',"basbenja@gmail.com", MOCK_AVATAR, MOCK_SOURCE_CODE),
        ('robot1',"juliolcese@gmail.com", MOCK_AVATAR, MOCK_SOURCE_CODE),
        ('robot2',"juliolcese@gmail.com", "", MOCK_SOURCE_CODE),
        ('robot1',"tonimondejar@gmail.com", "", MOCK_SOURCE_CODE),
        ('robot2',"tonimondejar@gmail.com", MOCK_AVATAR, MOCK_SOURCE_CODE),
        ('robot3',"tonimondejar@gmail.com", MOCK_AVATAR, MOCK_SOURCE_CODE)        
    ]

    for name, owner, avatar, source_code in robots:
        create_robot(
            NewRobot(
                name=name, 
                email=owner, 
                avatar=avatar, 
                source_code=source_code
            )
        )
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
        create_test_match(
            MatchTest(
                name=name, 
                creator_user=creator_user,
                creator_robot=creator_robot, 
                min_players=min_players,
                max_players=max_players, num_games=num_games, 
                num_rounds=num_rounds, password=password, 
                robots_joined=robots_joined
            )
        )
    return

def test_join_lobby():
    initial_users()
    initial_robots()
    initial_matches()
    
    match_id = get_match_by_name_and_user('match1', 'basbenja').match_id
    
    response = client.get(
        f'/matches/join-lobby/?match_id={match_id}',
        headers = {'Authorization': MOCK_TOKEN_BENJA},
    )
    
    print(response.json())
    
    assert response.status_code == 200
    assert response.json() == {
        'name': 'match1',
        'creator_username': 'basbenja',
        'min_players': 2,
        'max_players': 4,
        'num_games': 10,
        'num_rounds': 1570,
        'users_joined': 2,
        'user_robot': {'basbenja': 'robot1', 'jolcese': 'robot1'},
        'started': False
    }