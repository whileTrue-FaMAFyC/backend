import math
import numpy as np


COLLISION_DAMAGE = 2

# Meters advanced when moving at 1% velocity
M_VELOC_1 = 10

OUT_OF_BOUNDS = (1500,1500)

# The maximum possible distance between two robots is 1414 meters
# sqrt(1000^2 + 1000^2) = 1414,21
MAX_POSSIBLE_DISTANCE = 1415

ROUNDS_TO_RELOAD_CANNON_500_TO_700 = 4
ROUNDS_TO_RELOAD_CANNON_300_TO_500 = 3
ROUNDS_TO_RELOAD_CANNON_100_TO_300 = 2
ROUNDS_TO_RELOAD_CANNON_BELOW_100 = 1

IMPORT_ROBOT_CLASS = "from services.Robot import Robot\n"


class GameException(Exception):
    def __init__(self, detail):
        self.message = detail
        super().__init__(self.message)

        
def round_up(x):
    return np.sign(x)*(math.ceil(abs(x)))
