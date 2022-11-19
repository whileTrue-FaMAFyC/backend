from pony.orm import db_session

from database.models.models import RobotStats
from database.dao.robot_dao import get_robot_by_owner_and_name


@db_session
def get_stats_by_robot(owner_username: str, robot_name: str):
    robot = get_robot_by_owner_and_name(owner_username, robot_name)
    return RobotStats.get(robot=robot)
