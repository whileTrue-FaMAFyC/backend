import numpy as np
import math

COLLISION_DAMAGE = 2

# Meters advanced when moving at 1% velocity
M_VELOC_1 = 10

OUT_OF_BOUNDS = (1500,1500)


class GameException(Exception):
    def __init__(self, detail):
        self.message = detail
        super().__init__(self.message)

        
def round_up(x):
    return np.sign(x)*(math.ceil(abs(x)))
