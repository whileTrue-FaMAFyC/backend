import numpy as np
import math

def round_up(x):
    return np.sign(x)*(math.ceil(abs(x)))

COLLISION_DAMAGE = 2

# Meters advanced when moving at 1% velocity
M_VELOC_1 = 10

OUT_OF_BOUNDS = (1500,1500)

# The maximum possible distance between two robots is 1414 meters
# sqrt(1000^2 + 1000^2) = 1414,21
MAX_POSSIBLE_DISTANCE = 1415

class GameException(Exception):
    def __init__(self, detail):
        self.message = detail
        super().__init__(self.message)
