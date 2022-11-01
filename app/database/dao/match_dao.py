from passlib.hash import bcrypt
from pony.orm import db_session

from database.dao.match_results_dao import get_results_by_robot_and_match
from database.models.models import Match, Robot, User 
from utils.match_utils import match_winner
from view_entities.match_view_entities import *

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
def get_match_by_id(match_id: str):
    return Match[match_id]


@db_session
def get_all_matches():
    matches = Match.select()
    return matches


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
        
        if robot.owner.avatar == "default":
            user_robot.append(UserAndRobotInfo(
                username=robot.owner.username,
                user_avatar="",
                robot_name=robot.name,
                robot_avatar=robot.avatar
            ))    
        else:
            user_robot.append(UserAndRobotInfo(
                username=robot.owner.username,
                user_avatar=robot.owner.avatar,
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
