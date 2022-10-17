import numpy as np
import math

# Meters advanced when moving at 1% velocity
M_VELOC_1 = 10

def round_up(x):
    return np.sign(x)*(math.ceil(abs(x)))
