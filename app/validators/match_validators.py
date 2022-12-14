from fastapi import HTTPException, status
from pony.orm import db_session

from database.dao import match_dao, robot_dao
from utils.match_utils import *
from utils.robot_utils import get_robot_in_match_by_owner
from utils.user_utils import verify_password
from view_entities.match_view_entities import JoinMatch, NewMatch


def new_match_validator(creator_username: str, new_match: NewMatch):
    # To check if the user has a robot with the provided name
    users_robot = robot_dao.get_robot_by_owner_and_name(
        creator_username,
        new_match.creator_robot
    )
    # To check if the user already created a match with the provided name
    name_in_use = match_dao.get_match_by_name_and_user(
        new_match.name,
        creator_username
    )
    valid_match = True
    detail = ""

    if (len(new_match.name) < 3 or len(new_match.name) > 16):
        code = status.HTTP_400_BAD_REQUEST
        valid_match = False
        detail += "The match name has to have between 3 and 16 characters. "

    if (len(new_match.password) > 16):
        code = status.HTTP_400_BAD_REQUEST
        valid_match = False
        detail += "The password can't have more than 16 characters. "

    if (new_match.min_players < 2 or new_match.min_players > 4):
        code = status.HTTP_400_BAD_REQUEST
        valid_match = False
        detail += "Minimum amount of players has to be between 2 and 4. "

    if (new_match.max_players < 2 or new_match.max_players > 4):
        code = status.HTTP_400_BAD_REQUEST
        valid_match = False
        detail += "Maximum amount of players has to be between 2 and 4. "

    if (new_match.min_players > new_match.max_players):
        code = status.HTTP_400_BAD_REQUEST
        valid_match = False
        detail += "Minimum amount of players can't be greater than " \
                  "maximum amount of players. "

    if (new_match.num_games < 1 or new_match.num_games > 200):
        code = status.HTTP_400_BAD_REQUEST
        valid_match = False
        detail += "Number of games has to be between 1 and 200. "

    if (new_match.num_rounds < 1 or new_match.num_rounds > 10000):
        code = status.HTTP_400_BAD_REQUEST
        valid_match = False
        detail += "Number of rounds has to be between 1 and 10000. "

    if not (users_robot):
        code = status.HTTP_409_CONFLICT
        valid_match = False
        detail += f"Robot {new_match.creator_robot} isn't "\
                  f"in {creator_username}'s library. "

    if name_in_use:
        code = status.HTTP_409_CONFLICT
        valid_match = False
        detail += f"{creator_username} already has a match " \
                  f"named {new_match.name}. "

    if (not valid_match):
        raise HTTPException(
            status_code=code,
            detail=detail
        )

    return


def start_match_validator(creator_username: str, match_id: int):
    # Checks if the user trying to start the match is the creator
    match = match_validator_info(match_id)

    if not match_dao.get_match_by_id(match_id):
        raise INEXISTENT_MATCH_EXCEPTION

    if match.creator_username != creator_username:
        raise NOT_CREATOR

    # Checks if the match hasn't started yet
    if match.started:
        raise MATCH_ALREADY_STARTED

    # Checks if the minimum amount of players has been reached
    if match.robots_joined < match.min_players:
        raise NOT_ENOUGH_PLAYERS


@db_session
def leave_match_validator(match_id: int, leaving_username: str):
    robots_in_match = match_dao.select_robots_from_match_by_id(match_id)

    # If robots_in_match is empty, it means the match doesn't exists because
    # there is always at least one robot joined to a match (the creator).
    if not robots_in_match:
        raise INEXISTENT_MATCH_EXCEPTION

    match_creator = match_dao.get_match_creator_by_id(
        match_id
    ).creator_user.username

    if match_creator == leaving_username:
        raise CREATOR_CANT_ABANDON_EXCEPTION

    # Tries to get the robot with which the user joined the match.
    leaving_robot = get_robot_in_match_by_owner(match_id, leaving_username)

    if not leaving_robot:
        raise USER_NOT_JOINED_EXCEPTION

    return


def join_match_validator(username: str, match: JoinMatch, match_id: int):
    # To check if the user has a robot with the provided name
    joining_robot_in_db = robot_dao.get_robot_by_owner_and_name(
        username,
        match.joining_robot
    )
    # To check if the match exists
    match_in_db = match_dao.get_match_by_id(match_id)

    if not joining_robot_in_db:
        raise INEXISTENT_ROBOT

    if not match_in_db:
        raise INEXISTENT_MATCH_EXCEPTION

    # Check if user has already joined the match
    users_in_match = match_dao.get_users_in_match(match_id)
    if username in users_in_match:
        raise USER_ALREADY_JOINED

    if match.match_password == "":
        if match_in_db.hashed_password != "":
            raise INCORRECT_PASSWORD
    elif match_in_db.hashed_password == "":
        raise MATCH_DOES_NOT_HAVE_PASSWORD
    elif not verify_password(match.match_password, match_in_db.hashed_password):
        raise INCORRECT_PASSWORD

    if len(users_in_match) == match_in_db.max_players:
        raise MAX_PLAYERS_REACHED

    if match_in_db.started:
        raise MATCH_ALREADY_STARTED
