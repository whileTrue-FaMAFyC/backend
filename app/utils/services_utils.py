import numpy as np
import math
from typing import List
from base64 import b64decode 

from database.dao.robot_dao import get_source_code_by_id

def round_up(x):
    return np.sign(x)*(math.ceil(abs(x)))

COLLISION_DAMAGE = 2
# Meters advanced when moving at 1% velocity
M_VELOC_1 = 10

OUT_OF_BOUNDS = (1500,1500)

ROUNDS_TO_RELOAD_CANNON_500_TO_700 = 4
ROUNDS_TO_RELOAD_CANNON_300_TO_500 = 3
ROUNDS_TO_RELOAD_CANNON_100_TO_300 = 2
ROUNDS_TO_RELOAD_CANNON_BELOW_100 = 1

IMPORT_ROBOT_CLASS = "from services.Robot import Robot\n"

class GameException(Exception):
    def __init__(self, detail):
        self.message = detail
        super().__init__(self.message)

def extract_filename_from_file(source_code_in_db):
    filename = source_code_in_db.split(";")[0].replace("name:", "")
    source_code = source_code_in_db.split("base64,")[1]
    return filename, source_code

def extract_class_name(filename):
    without_ = filename.split("_")
    for i in range(len(without_)):
        without_[i] = without_[i].capitalize()
    class_name = ''.join(without_)
    return class_name[:len(class_name)-3]

def create_robots_instances(robots_id: List[int]):
    robots = []
    robot = ""
    for r in robots_id:
        source_code_in_db = get_source_code_by_id(r)
        filename, source_code_b64 = extract_filename_from_file(source_code_in_db)
        source_code = IMPORT_ROBOT_CLASS + b64decode(source_code_b64)
        exec(source_code)
        class_name = extract_class_name(filename)
        exec(f"robot = {class_name}(robot_id={r})")
        robots.append(robot)
    return robots
