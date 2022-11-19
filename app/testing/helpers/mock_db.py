from pony.orm import db_session
from passlib.hash import bcrypt

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



# NOTE: unverified users shouldn't have matches nor robots
@db_session
def users():
    users = [
        ('bas_benja', 'basbenja3@gmail.com', MOCK_AVATAR,
         'Compuamigos2', 555888, True, datetime.now()),
        ('juliolcese', 'juliolcese@mi.unc.edu.ar', MOCK_AVATAR,
         '1whileTrue1', 889654, True, MOCK_CREATED_TIME),
        ('tonimondejar', 'mondejarantonio@hotmail.com',
         "", 'FAMAFyC2022', 853314, True, datetime.now()),
        ('valennegrelli', 'valen57negrelli@yahoo.com.ar',
         "", 'piXies18', 852436, True, MOCK_CREATED_TIME),
        ('lucasca22ina', 'cassinalucas@gmail.com', "",
         'chicosSSS1456', 152347, True, datetime.now()),
        ('sebagiraudo', 'sebagir4udo@unc.edu.ar', MOCK_AVATAR,
         'B_1kerfuliate', 123456, False, MOCK_CREATED_TIME),
        ('israangulo4', 'isra1234@hotmail.com', MOCK_AVATAR,
         'Argentiña222', 785364, False, MOCK_CREATED_TIME),
        ('pyrobots', 'pyrobots.notreply@gmail.com',
         MOCK_AVATAR, 'Test1234', 525600, True, datetime.now())
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
robot_crack_source_code = "name:robot_capo_crack.py;base64,Y2xhc3MgUm9ib3RDYXBvQ3JhY2"\
                          "soUm9ib3QpOg0KDQogICAgZGVmIGluaXRpYWxpemUoc2VsZik6DQogICAg"\
                          "ICAgIHNlbGYuZm91bmRfcm9ib3QgPSBGYWxzZQ0KICAgICAgICBzZWxmLm"\
                          "RlZ3JlZXMgPSAwDQoNCiAgICBkZWYgcmVzcG9uZChzZWxmKToNCiAgICAg"\
                          "ICAgaWYgbm90IHNlbGYuc2Nhbm5lZCgpOg0KICAgICAgICAgICAgIyBDaG"\
                          "FuZ2Ugc2NhbiBkZWdyZWVzIHVudGlsIGZpbmRpbmcgc29tZW9uZQ0KICAg"\
                          "ICAgICAgICAgc2VsZi5kZWdyZWVzICs9IDIwIA0KICAgICAgICAgICAgc2"\
                          "VsZi5wb2ludF9zY2FubmVyKHNlbGYuZGVncmVlcywgMTApDQogICAgICAg"\
                          "IGVsc2U6DQogICAgICAgICAgICBpZiBzZWxmLnNjYW5uZWQoKSA+IDcwMD"\
                          "oNCiAgICAgICAgICAgICAgICBzZWxmLmRyaXZlKHNlbGYuZGVncmVlcywg"\
                          "MTApDQogICAgICAgICAgICBlbHNlOg0KICAgICAgICAgICAgICAgIHNlbG"\
                          "YuZHJpdmUoc2VsZi5kZWdyZWVzLCAwKQ0KICAgICAgICAgICAgICAgIHNl"\
                          "bGYuY2Fubm9uKHNlbGYuZGVncmVlcywgc2VsZi5zY2FubmVkKCkpDQo="

robot_inutil_source_code = "name:robot_inutil.py;base64,Y2xhc3MgUm9ib3RJbnV0aWwoUm9ib"\
                           "3QpOg0KICAgIGRlZiBpbml0aWFsaXplKHNlbGYpOg0KICAgICAgICBwYX"\
                           "NzDQogICAgDQogICAgZGVmIHJlc3BvbmQoc2VsZik6DQogICAgICAgIHB"\
                           "hc3MNCg=="


@db_session
def robots():
    robots = [
        ('world_destroyer_29', MOCK_SOURCE_CODE, 'lucasca22ina', MOCK_AVATAR),
        ('_theTERMINATOR', MOCK_SOURCE_CODE, 'lucasca22ina', MOCK_AVATAR),
        ('R2D2', MOCK_SOURCE_CODE, 'valennegrelli', MOCK_AVATAR),
        ('WALL-E', MOCK_SOURCE_CODE, 'valennegrelli', ""),
        ('jarvis22', MOCK_SOURCE_CODE, 'valennegrelli', MOCK_AVATAR),
        ('0ptimusPrime', robot_inutil_source_code, 'bas_benja', MOCK_AVATAR),
        ('Bumblebee', robot_crack_source_code, 'bas_benja', MOCK_AVATAR),
        ('pichon', TEST_SOURCE_CODE_BENJA, 'bas_benja', MOCK_AVATAR),
        ('_tron', MOCK_SOURCE_CODE, 'tonimondejar', MOCK_AVATAR),
        ('MegaByte', MOCK_SOURCE_CODE, 'tonimondejar', MOCK_AVATAR),
        ('CYborg34', TEST_SOURCE_CODE_TONI, 'tonimondejar', MOCK_AVATAR),
        ('automatax', TEST_SOURCE_CODE_JULI, 'juliolcese', MOCK_AVATAR),
        ('astroGirl', MOCK_SOURCE_CODE, 'juliolcese', MOCK_AVATAR),
        ('RobotCrack', robot_crack_source_code, 'juliolcese', MOCK_AVATAR),
        ('RobotInutil', robot_inutil_source_code, 'bas_benja', MOCK_AVATAR),
        ('RobotInutil', robot_inutil_source_code, 'lucasca22ina', MOCK_AVATAR)
    ]

    for robot_name, source_code, username, avatar in robots:
        robot = Robot(
            name=robot_name,
            source_code=source_code,
            owner=get_user_by_username(username),
            avatar=avatar
        )
        robot_stats = RobotStats(
            robot=robot
        )
        robot.set(stats=robot_stats)
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
          RobotInMatch(
             owner=UserInMatch(
                 username="bas_benja"),
             name="Bumblebee"),
             RobotInMatch(owner=UserInMatch(username="juliolcese"), name="automatax")]),

        ('partidaza', 'valennegrelli', 'R2D2', 2, 2, 200, 1, "", False,
         [RobotInMatch(owner=UserInMatch(username="valennegrelli"), name="R2D2"),
          RobotInMatch(owner=UserInMatch(username="bas_benja"), name="Bumblebee")])
    ]

    for (name, creator_user, creator_robot, min_players, max_players,
         num_games, num_rounds, password, started, robots_joined) in matches:
        set_robots = set()
        for r in robots_joined:
            set_robots.add(get_robot_by_owner_and_name(r.owner.username, r.name))

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
                    ("Bumblebee", "bas_benja", "match!",
                     "tonimondejar", 75, 25, 100),
                    ("automatax", "juliolcese", "match!", "tonimondejar", 0, 0, 200)]

    for (robot_name, robot_owner, match_name, match_owner,
         games_won, games_tied, games_lost) in match_result:

        MatchResult(
            robot=get_robot_by_owner_and_name(robot_owner, robot_name),
            match=get_match_by_name_and_user(match_name, match_owner),
            games_won=games_won,
            games_tied=games_tied,
            games_lost=games_lost
        )

    return
