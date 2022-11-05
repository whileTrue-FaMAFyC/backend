from random import randint
from typing import List

from services.game import Game, Missile
from testing.helpers.services_helpers import *


robots: List[RobotTest] = [Robot1(1,0), Robot2(2,0), Robot3(3,0), Robot4(4,0)]

robots[0].set_initial_position(802, 798)
robots[1].set_initial_position(234, 799)
robots[2].set_initial_position(243, 52)
robots[3].set_initial_position(101, 64)

missiles = [
    # Hits robots[0] with damage 10 (distance = 25)
    Missile(0,(799,799), (799,799), randint(0,360), randint(0,700)),
    
    # Hits robots[0] with damage 10 (distance = 25)
    Missile(0,(798,798), (798,798), randint(0,360), randint(0,700)),
    
    # Hits robots[1] with damage 5 (distance = 50)
    Missile(0,(221,840), (221,840), randint(0,360), randint(0,700)),
    
    # Hits robots[1] with damage 3 (distance = 100)
    Missile(0,(300,800), (300,800), randint(0,360), randint(0,700)),
    
    # Hit robots[2] with damage 3 (distance = 100) 
    # and robots[3] with damage 3 (distance = 100)
    Missile(0,(166,8), (166,8), randint(0,360), randint(0,700))
]

game = Game(100, robots)

def test_inflict_different_damages():
    for m in missiles:
        game._inflict_damage(m)
    
    assert robots[0].get_damage() == 20
    assert robots[1].get_damage() == 8
    assert robots[2].get_damage() == 3
    assert robots[3].get_damage() == 3


def test_inflict_no_damage():
    game._inflict_damage(
        # Current position is not the same as final position
        Missile(0,(799,799), (500,256), randint(0,360), randint(0,700))
    )
    
    assert robots[0].get_damage() == 20
    assert robots[1].get_damage() == 8
    assert robots[2].get_damage() == 3
    assert robots[3].get_damage() == 3
