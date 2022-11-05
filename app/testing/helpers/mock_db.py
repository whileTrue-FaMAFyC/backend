from pony.orm import db_session
from passlib.hash import bcrypt
from random import choice

from database.models.models import *
from database.dao.match_dao import *
from database.dao.robot_dao import *
from database.dao.user_dao import *
from view_entities.robot_view_entities import RobotInMatch
from view_entities.user_view_entities import UserInMatch

def mock_avatar(username: str):
    return f'../assets/users/{username}/avatar.png'

def mock_bot_avatar(username: str, bot_filename: str):
    return f'../assets/users/{username}/avatar_{bot_filename}.png'

def mock_source_code(filename: str):
    return f'../assets/model_robots/{filename}'

MOCK_CREATED_TIME = datetime.now() - timedelta(hours=5)

MOCK_FILENAMES = ['cool_robot.py', 'dumb_robot.py', 'running_robot.py', 'shooter_robot.py']

@db_session
def users():
    users = [
        ('bas_benja', 'basbenja3@gmail.com', mock_avatar('bas_benja'), 'Compuamigos2', 555888, True, datetime.now()),
        ('juliolcese', 'juliolcese@mi.unc.edu.ar', mock_avatar('juliolcese'), '1whileTrue1', 889654, True, MOCK_CREATED_TIME),
        ('tonimondejar', 'mondejarantonio@hotmail.com', 'default', 'FAMAFyC2022', 123456, False, MOCK_CREATED_TIME),
        ('valennegrelli', 'valen57negrelli@yahoo.com.ar', 'default', 'piXies18', 852436, False, MOCK_CREATED_TIME),
        ('sebagiraudo', 'sebagir4udo@unc.edu.ar', mock_avatar('sebagiraudo'), 'B_1kerfuliate', 785364, True, datetime.now()),
        ('lucasca22ina', 'cassinalucas@gmail.com', 'default', 'chicosSSS1456', 152347, True, datetime.now()),
        ('israangulo4', 'isra1234@hotmail.com', mock_avatar('israangulo4'), 'Argentiña222', 853314, False, datetime.now())
    ]
    
    for username, email, avatar, password, verification_code, verified, created_time in users:
        User(
            username=username,
            email=email,
            avatar=avatar,
            hashed_password=bcrypt.hash(password),
            verification_code=verification_code,
            verified=verified,
            created_time=created_time
        )
    return
            
# Add some robots to the database
@db_session
def robots():
    robots = [
        ('robot_cool', 'israangulo4', ''),
        ('world_destroyer_29', 'lucasca22ina', ''),
        ('_theTERMINATOR', 'lucasca22ina', ''),
        ('R2D2', 'valennegrelli', mock_bot_avatar('valennegrelli', 'dumb_robot.py')),
        ('WALL-E', 'valennegrelli', 'default'),
        ('jarvis22', 'valennegrelli', mock_bot_avatar('valennegrelli', 'running_robot.py')),
        ('0ptimusPrime', 'bas_benja', mock_bot_avatar('bas_benja', 'shooter_robot.py')),
        ('Bumblebee', 'bas_benja', ''),
        ('_tron', 'tonimondejar', 'default'),
        ('MegaByte', 'tonimondejar', ''),
        ('CYborg34', 'tonimondejar', ''),
        ('automatax', 'juliolcese', ''),
        ('astroGirl', 'juliolcese', mock_bot_avatar('astroGirl', 'cool_robot.py'))
    ]

    for robot_name, owner_username, avatar in robots:
        source_code = choice(MOCK_FILENAMES)
        Robot(
            name=robot_name,
            source_code=mock_source_code(source_code),
            owner=get_user_by_username(owner_username),
            avatar=mock_bot_avatar(owner_username, source_code) if avatar == '' else avatar
        )
    return

@db_session
def matches():
    matches = [
        ('match1', 'bas_benja', '0ptimusPrime', 2, 4, 10, 1570, "", False,
        [RobotInMatch(owner=UserInMatch(username="bas_benja"), name="0ptimusPrime"), 
         RobotInMatch(owner=UserInMatch(username="juliolcese"), name="astroGirl")]),
        
        ('match2', 'bas_benja', 'Bumblebee', 3, 3, 200, 100000, "matchPass!", False, 
        [RobotInMatch(owner=UserInMatch(username="bas_benja"), name="Bumblebee")]),
        
        ('match1', 'juliolcese', 'astroGirl', 2, 3, 1, 1, "P455W0RD", False,
        [RobotInMatch(owner=UserInMatch(username="juliolcese"), name="astroGirl")]),
        
        ('jmatch2', 'juliolcese', 'automatax', 2, 3, 1, 1, "P455W0RD", False,
        [RobotInMatch(owner=UserInMatch(username="juliolcese"), name="automatax")]),
        
        ('24601', 'tonimondejar', 'MegaByte', 2, 2, 157, 3250, "", False,
        [RobotInMatch(owner=UserInMatch(username="tonimondejar"), name="MegaByte")]),
        
        ('match!', 'tonimondejar', '_tron', 3, 4, 200, 1, "pw", True,
         [RobotInMatch(owner=UserInMatch(username="tonimondejar"), name="_tron"), 
         RobotInMatch(owner=UserInMatch(username="bas_benja"), name="Bumblebee"), 
         RobotInMatch(owner=UserInMatch(username="juliolcese"), name="automatax")])
    ]

    for (name, creator_user, creator_robot, min_players, max_players, 
         num_games, num_rounds, password, started, robots_joined) in matches:
        set_robots = set()
        for r in robots_joined:
            set_robots.add(get_bot_by_owner_and_name(r.owner.username, r.name))
        
        Match(
            name=name,
            creator_user=get_user_by_username(creator_user),
            min_players=min_players,
            max_players=max_players,
            num_games=num_games,
            num_rounds=num_rounds,
            started=started,
            hashed_password=bcrypt.hash(password) if password else "",
            robots_joined=set_robots
        )       
    
    return

@db_session
def match_result():
    match_result = [("_tron", "tonimondejar", "match!", "tonimondejar", 100, 25, 75),
                    ("Bumblebee", "bas_benja", "match!", "tonimondejar", 75, 25, 100),
                    ("automatax", "juliolcese", "match!", "tonimondejar", 0, 0, 200)]

    for (robot_name, robot_owner, match_name, match_owner, 
         games_won, games_tied, games_lost) in match_result:
        
        MatchResult(
            robot = get_bot_by_owner_and_name(robot_owner, robot_name),
            match = get_match_by_name_and_user(match_name, match_owner),
            games_won = games_won,
            games_tied = games_tied,
            games_lost = games_lost
        )       
    
    return