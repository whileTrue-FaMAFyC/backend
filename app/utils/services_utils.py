from base64 import b64decode
import math
from numpy import add, sign
from typing import List, Tuple

from database.dao.robot_dao import get_source_code_by_id


ROBOT_SIZE = 32

ROBOT_HALF_SIZE = int(ROBOT_SIZE/2)

COLLISION_DAMAGE = 2

MISSILE_HALF_SIZE = 10

# Meters advanced when moving at 1% velocity
M_VELOC_1 = 3

# Meters a missile advances in a round
MISSILE_ADVANCE = 100

OUT_OF_BOUNDS = (1500,1500)

# The maximum possible distance between two robots is 1414 meters
# sqrt(1000^2 + 1000^2) = 1414,21
MAX_POSSIBLE_DISTANCE = 1415

ROUNDS_TO_RELOAD_CANNON_BELOW_100 = 2
ROUNDS_TO_RELOAD_CANNON_100_TO_300 = ROUNDS_TO_RELOAD_CANNON_BELOW_100 + 1
ROUNDS_TO_RELOAD_CANNON_300_TO_500 = ROUNDS_TO_RELOAD_CANNON_100_TO_300 + 1
ROUNDS_TO_RELOAD_CANNON_500_TO_700 = ROUNDS_TO_RELOAD_CANNON_300_TO_500 + 1

DISTANCE_DAMAGE_10 = 25
DISTANCE_DAMAGE_5 = 50
DISTANCE_DAMAGE_3 = 100

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


def create_robots_instances(robots_id):
    robots = []
    r_id_in_game = 0
    for r in robots_id:
        source_code_in_db = get_source_code_by_id(r)
        filename, source_code_b64 = extract_filename_from_file(source_code_in_db)
        class_name = extract_class_name(filename)
        source_code = IMPORT_ROBOT_CLASS + b64decode(source_code_b64).decode("utf-8") 
        exec(source_code)
        exec(f"\nrobot = {class_name}(robot_id={r}, id_in_game={r_id_in_game})\nrobots.append(robot)")
        r_id_in_game += 1
    return robots


def round_up(x):
    return sign(x)*(math.ceil(abs(x)))


def get_vertex(center: Tuple[int, int]):
    return [tuple(add(center, (-ROBOT_HALF_SIZE, -ROBOT_HALF_SIZE))), 
            tuple(add(center, (ROBOT_HALF_SIZE, -ROBOT_HALF_SIZE))),
            tuple(add(center, (ROBOT_HALF_SIZE, ROBOT_HALF_SIZE))),
            tuple(add(center, (-ROBOT_HALF_SIZE, ROBOT_HALF_SIZE)))]


def is_inside(vertexs: List[Tuple[int, int]], center: Tuple[int, int]):
    is_inside = False
    
    for v in vertexs:
        check_x = v[0] in range(center[0]-ROBOT_HALF_SIZE, 1+center[0]+ROBOT_HALF_SIZE)
        check_y = v[1] in range(center[1]-ROBOT_HALF_SIZE, 1+center[1]+ROBOT_HALF_SIZE)
        is_inside = check_x and check_y
        if is_inside:
            break

    return is_inside


# Problem with this one: the changes made on the instance doesn't have effect
# import multiprocessing
# def timeout_decorator(robot, func):
#     # Start bar as a process
#     p = multiprocessing.Process(target=func)
#     p.start()

#     # Wait for 10 seconds or until process finishes
#     p.join(10)

#     # If thread is still active
#     if p.is_alive():
#         print('Timeout reached! Killing robot')
#         robot._increase_damage(100)
#         p.terminate()
#         p.join()

# Problem with this one: only works on certains OS
import signal
def timeout_decorator(robot, func):
    def handler(signum, frame):
        raise Exception('timeout!')

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(1)

    try:
        func()
    except Exception as exc:
        robot._damage = 100
        print(exc)
    finally:
        signal.alarm(0)
