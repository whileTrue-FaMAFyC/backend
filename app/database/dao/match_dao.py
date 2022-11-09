from passlib.hash import bcrypt
from pony.orm import db_session, select

from database.dao.match_results_dao import get_results_by_robot_and_match
from database.models.models import Match, Robot, User
from utils.match_utils import match_winner 
from utils.robot_utils import get_robot_in_match_by_owner
from view_entities.robot_view_entities import *
from view_entities.match_view_entities import *
from utils.match_utils import match_winner

@db_session
def create_new_match(creator_username, new_match: NewMatch):
    creator = User.get(username=creator_username)
    robot_creator = Robot.get(name=new_match.creator_robot, owner=creator)
    
    match_password = bcrypt.hash(new_match.password) if new_match.password else ""
    
    try:
        Match(
            name=new_match.name,
            creator_user=creator,
            robots_joined=[robot_creator],
            min_players=new_match.min_players,
            max_players=new_match.max_players,
            num_games=new_match.num_games,
            num_rounds=new_match.num_rounds,
            started=False,
            hashed_password=match_password
        )
        return True
    except:
        return False


@db_session
def get_match_by_name_and_user(match_name: str, creator_username: str):
    matches = Match.get(creator_user=User.get(username=creator_username), 
                        name=match_name)
    return matches


@db_session
def get_match_by_id(match_id: int):
    return Match.get(match_id=match_id)


@db_session
def get_all_matches():
    matches = Match.select()
    return matches

@db_session
def get_match_info(match_id: int):
    match_details = Match[match_id]
    robots = []
    for r in match_details.robots_joined:
        robots.append(RobotPlayer.from_orm(r))

    return StartMatch(
        num_games=match_details.num_games, 
        num_rounds=match_details.num_rounds, 
        robots_joined=robots
    )

@db_session
def update_executed_match(match_id: int):
    try:
        match = Match[match_id]
        match.set(started=True)
        return True
    except:
        return False

@db_session
def update_leaving_user(match_id: int, leaving_user: str):
    
    match = Match.get(match_id=match_id)

    robot = get_robot_in_match_by_owner(match_id, leaving_user)
    
    try:
        match.robots_joined.remove(robot)
        return True
    except:
        return False

@db_session
def get_users_in_match(match_id: int):
    match_in_db = Match[match_id]
    users = []
    for r in match_in_db.robots_joined:
        users.append(r.owner.username)
    return users

@db_session
def update_joining_user_match(joining_username: str, joining_robot: str, match_id: int):
    match_in_db = Match[match_id]

    joining_user_in_db = User.get(username=joining_username)

    joining_robot_in_db = Robot.get(name=joining_robot, owner=joining_user_in_db)

    try:
        match_in_db.robots_joined.add(joining_robot_in_db)
        return True
    except:
        return False


@db_session
def get_lobby_info(match_id: int, username: str):
    match: Match = Match[match_id]
    creator_username = match.creator_user.username
    results = []
    robots_id = []
    game_results = {}
    has_password = False

    im_in = False
    user_robot = []
    for robot in match.robots_joined:
        if match.started:
            robot_id = robot.robot_id
            robots_id.append(robot_id)
            game_results[robot_id] = get_results_by_robot_and_match(robot_id, match_id)

        if robot.owner.username == username:
            im_in = True
        
        user_robot.append(UserAndRobotInfo(
                username=robot.owner.username,
                user_avatar= "" if (robot.owner.avatar == "default") else robot.owner.avatar,
                robot_name=robot.name,
                robot_avatar=robot.avatar
        ))
    
    if match.started:
        results = match_winner(robots_id, game_results)

    if match.hashed_password != "":
        has_password = True

    return LobbyInfo(
        requester_username=username,
        name=match.name,
        creator_username=creator_username,
        min_players=match.min_players,
        max_players=match.max_players,
        num_games=match.num_games,
        num_rounds=match.num_rounds,
        users_joined=len(user_robot),
        user_robot=user_robot,
        started=match.started,
        im_in=im_in,
        is_creator=(creator_username==username),
        results=results,
        has_password=has_password
    )

@db_session
def get_match_creator_by_id(match_id: int):

    return Match.get(match_id=match_id)

@db_session
def select_robots_from_match_by_id(match_id: int):
    
    return select(m.robots_joined for m in Match 
                  if m.match_id == match_id)

@db_session
def update_joining_user_match(joining_username: str, joining_robot: str, match_id: int):
    match_in_db = Match[match_id]

    joining_user_in_db = User.get(username=joining_username)

    joining_robot_in_db = Robot.get(name=joining_robot, owner=joining_user_in_db)

    try:
        match_in_db.robots_joined.add(joining_robot_in_db)
        return True
    except:
        return False

@db_session
def get_matches_with_filter(is_owner: bool, is_joined: bool, started: bool, user: str):
    q = Match.select()

    if is_owner == True:
        q = q.filter(lambda m: m.creator_user.username == user)
    elif is_owner == False:
        q = q.filter(lambda m: m.creator_user.username != user)
    
    if is_joined == True:
        q = q.filter(lambda m: user in (rj.owner.username for rj in m.robots_joined))
    elif is_joined == False:
        q = q.filter(lambda m: not (user in (rj.owner.username for rj in m.robots_joined)))
        
    if started == True:
        q = q.filter(lambda m: m.started)
    elif started == False:
        q = q.filter(lambda m: not m.started)
    
    return q