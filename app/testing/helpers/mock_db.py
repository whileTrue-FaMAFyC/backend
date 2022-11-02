from pony.orm import db_session
from passlib.hash import bcrypt
from app.database.dao.match_dao import get_match_by_name_and_user

from database.models.models import *
from database.dao.match_dao import *
from database.dao.robot_dao import *
from database.dao.user_dao import *
from view_entities.robot_view_entities import RobotInMatch
from view_entities.user_view_entities import UserInMatch

MOCK_SOURCE_CODE = """aW1wb3J0IHV2aWNvcm4KCgppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgog
                    ICAgdXZpY29ybi5ydW4oImFwcC5hcGk6YXBwIiwgaG9zdD0iMC4wLjAuMCIs
                    IHBvcnQ9ODAwMCwgcmVsb2FkPVRydWUp"""
MOCK_AVATAR = """iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQ
                DwAEhQGAhKmMIQAAAABJRU5ErkJggg=="""

MOCK_CREATED_TIME = datetime.now() - timedelta(hours=5)

TEST_SOURCE_CODE_TONI = """name:robot_test.py;base64,Y2xhc3MgUm9ib3RUZXN0KFJvYm9
                    0KToKICAgIGRlZiBpbml0aWFsaXplKHNlbGYpOgogICAgICAgIHNlbGYudGV
                    zdF92YXJpYWJsZSA9ICdTb3kgZWwgcm9ib3QgZGUgdG9uaScKICAgIGRlZiB
                    yZXNwb25kKCk6CiAgICAgICAgcGFzcw=="""

TEST_SOURCE_CODE_JULI = """name:robot_test.py;base64,Y2xhc3MgUm9ib3RUZXN0KFJvYm9
                    0KToKICAgIGRlZiBpbml0aWFsaXplKHNlbGYpOgogICAgICAgIHNlbGYudGV
                    zdF92YXJpYWJsZSA9ICJTb3kgZWwgcm9ib3QgZGUganVsaSIKICAgIGRlZiB
                    yZXNwb25kKCk6CiAgICAgICAgcGFzcw=="""

TEST_SOURCE_CODE_BENJA = """name:robot_test.py;base64,Y2xhc3MgUm9ib3RUZXN0KFJvYm
                    90KToKICAgIGRlZiBpbml0aWFsaXplKHNlbGYpOgogICAgICAgIHNlbGYudG
                    VzdF92YXJpYWJsZSA9ICJTb3kgZWwgcm9ib3QgZGUgYmVuamEiCiAgICBkZW
                    YgcmVzcG9uZCgpOgogICAgICAgIHBhc3M="""
@db_session
def users():
    users = [
        ('bas_benja', 'basbenja3@gmail.com', MOCK_AVATAR, 'Compuamigos2', 555888, True, datetime.now()),
        ('juliolcese', 'juliolcese@mi.unc.edu.ar', MOCK_AVATAR, '1whileTrue1', 889654, True, MOCK_CREATED_TIME),
        ('tonimondejar', 'mondejarantonio@hotmail.com', "", 'FAMAFyC2022', 123456, False, MOCK_CREATED_TIME),
        ('valennegrelli', 'valen57negrelli@yahoo.com.ar', "", 'piXies18', 852436, False, MOCK_CREATED_TIME),
        ('sebagiraudo', 'sebagir4udo@unc.edu.ar', MOCK_AVATAR, 'B_1kerfuliate', 785364, True, datetime.now()),
        ('lucasca22ina', 'cassinalucas@gmail.com', "", 'chicosSSS1456', 152347, True, datetime.now()),
        ('israangulo4', 'isra1234@hotmail.com', MOCK_AVATAR, 'Argentiña222', 853314, False, datetime.now())
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
        ('robot_cool', MOCK_SOURCE_CODE, 'isra1234@hotmail.com', MOCK_AVATAR),
        ('world_destroyer_29', MOCK_SOURCE_CODE, 'cassinalucas@gmail.com', MOCK_AVATAR),
        ('_theTERMINATOR', MOCK_SOURCE_CODE, 'cassinalucas@gmail.com', MOCK_AVATAR),
        ('R2D2', MOCK_SOURCE_CODE, 'valen57negrelli@yahoo.com.ar', MOCK_AVATAR),
        ('WALL-E', MOCK_SOURCE_CODE, 'valen57negrelli@yahoo.com.ar', ""),
        ('jarvis22', MOCK_SOURCE_CODE, 'valen57negrelli@yahoo.com.ar', MOCK_AVATAR),
        ('0ptimusPrime', MOCK_SOURCE_CODE, 'basbenja3@gmail.com', MOCK_AVATAR),
        ('Bumblebee', TEST_SOURCE_CODE_BENJA, 'basbenja3@gmail.com', MOCK_AVATAR),
        ('_tron', MOCK_SOURCE_CODE, 'mondejarantonio@hotmail.com', MOCK_AVATAR),
        ('MegaByte', MOCK_SOURCE_CODE, 'mondejarantonio@hotmail.com', MOCK_AVATAR),
        ('CYborg34', TEST_SOURCE_CODE_TONI, 'mondejarantonio@hotmail.com', MOCK_AVATAR),
        ('automatax', TEST_SOURCE_CODE_JULI, 'juliolcese@mi.unc.edu.ar', MOCK_AVATAR),
        ('astroGirl', MOCK_SOURCE_CODE, 'juliolcese@mi.unc.edu.ar', MOCK_AVATAR)
    ]

    for robot_name, source_code, owner_email, avatar in robots:
        Robot(
            name=robot_name,
            source_code=source_code,
            owner=get_user_by_email(owner_email),
            avatar=avatar
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
         RobotInMatch(owner=UserInMatch(username="juliolcese"), name="automatax")]),

        ('partidaza', 'valennegrelli', 'R2D2', 2, 2, 200, 1, "", False,
         [RobotInMatch(owner=UserInMatch(username="valennegrelli"), name="R2D2"), 
         RobotInMatch(owner=UserInMatch(username="bas_benja"), name="Bumblebee")])

    
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