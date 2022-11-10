from pony.orm import db_session, select

from database.dao.user_dao import get_user_by_username
from database.models.models import Robot, RobotStats
from utils.robot_utils import insert_filename_to_file
from view_entities.robot_view_entities import BotCreate, WinnerRobot


@db_session 
def get_bot_by_owner_and_name(owner_username: str, bot_name: str):
    return Robot.get(owner=get_user_by_username(owner_username), name=bot_name)


# The exsitance and validation of the username was previously validated,
# i.e. for this function we can assume that the user exists and is verified
@db_session
def create_new_bot(owner_username: str, bot_data: BotCreate):
    try:
        new_robot = Robot(
            name=bot_data.name,
            source_code=insert_filename_to_file(
                bot_data.source_code, 
                bot_data.bot_filename
            ),
            owner=get_user_by_username(owner_username),
            avatar=bot_data.avatar
        )
        new_robot_stats = RobotStats(
            robot=new_robot
        )
        new_robot.set(stats=new_robot_stats)
        return True
    except:
        return False


@db_session 
def get_bots_by_owner(owner_username: str):
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
def get_bot_by_id(robot_id: int):
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
