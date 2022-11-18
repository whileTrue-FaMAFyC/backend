from pony.orm import db_session

from database.dao.user_dao import get_user_by_username
from database.models.models import Robot, RobotStats
from utils.random_default_utils import *
from utils.robot_utils import insert_filename_to_file
from utils.shooter_default_utils import *
from view_entities.robot_view_entities import RobotCreate, WinnerRobot


@db_session
def get_robot_by_owner_and_name(owner_username: str, robot_name: str):
    return Robot.get(
        owner=get_user_by_username(owner_username),
        name=robot_name
    )


# The existance and validation of the username was previously validated,
# i.e. for this function we can assume that the user exists and is verified
@db_session
def create_new_robot(owner_username: str, robot_data: RobotCreate):
    try:
        new_robot = Robot(
            name=robot_data.name,
            source_code=insert_filename_to_file(
                robot_data.source_code,
                robot_data.bot_filename
            ),
            owner=get_user_by_username(owner_username),
            avatar=robot_data.avatar
        )
        new_robot_stats = RobotStats(
            robot=new_robot
        )
        new_robot.set(stats=new_robot_stats)
        return True
    except BaseException:
        return False


@db_session
def get_robots_by_owner(owner_username: str):
    return Robot.select(owner=get_user_by_username(owner_username))


@db_session
def get_name_and_creator_by_id(robot_id: int):
    robot = Robot[robot_id]

    return WinnerRobot(
        username=robot.owner.username,
        robot_name=robot.name
    )


@db_session
def get_robot_avatar_by_name_and_owner(owner: str, name: str):
    return Robot.get(owner=get_user_by_username(owner), name=name).avatar


@db_session
def get_source_code_by_id(robot_id: int):
    return Robot[robot_id].source_code


@db_session
def get_robot_by_id(robot_id: int):
    return Robot.get(robot_id=robot_id)


@db_session
def get_name_and_creator_by_id(robot_id: int):
    robot = Robot[robot_id]
    # return WinnerRobot(
    #     username=robot.owner.username,
    #     robot_name=robot.name
    # )
    return {
        "username": robot.owner.username,
        "robot_name": robot.name
    }


@db_session
def add_default_robots(username: str):
    try:
        create_new_robot(
            username,
            RobotCreate(
                name="Shooter",
                source_code=SHOOTER_SOURCE_CODE,
                bot_filename="shooter_robot.py",
                avatar=SHOOTER_AVATAR
            )
        )
        create_new_robot(
            username,
            RobotCreate(
                name="Random",
                source_code=RANDOM_SOURCE_CODE,
                bot_filename="random_robot.py",
                avatar=RANDOM_AVATAR
            )
        )
        return True
    except BaseException:
        return False
