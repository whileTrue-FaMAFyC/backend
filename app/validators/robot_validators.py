from database.dao.robot_dao import get_robot_by_owner_and_name
from utils.robot_utils import ROBOT_NAME_EXCEPTION

# Checks if 'username' already has a robot named 'robot_name'
def new_robot_validator(owner_username: str, robot_name: str):
    valid = get_robot_by_owner_and_name(owner_username, robot_name)
    # If valid is not None, it means that 'user' already has a robot named
    # 'robot_name'
    if valid is not None:
        raise ROBOT_NAME_EXCEPTION
