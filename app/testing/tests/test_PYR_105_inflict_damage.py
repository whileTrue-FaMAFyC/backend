from random import randint
from services.game import Game, Missile
from testing.helpers.services_helpers import *


robots: list[RobotTest] = [Robot1(1), Robot2(2), Robot3(3), Robot4(4)]

robots[0].set_initial_position(802,798)
robots[1].set_initial_position(234, 799)
robots[2].set_initial_position(123,50)
robots[3].set_initial_position(101, 64)

missiles = [
    # Hits robots[0] with damage 10
    Missile((799,799), (799,799), randint(0,360), randint(0,700)),
    
    # Hits robots[0] with damage 10
    Missile((798,798), (798,798), randint(0,360), randint(0,700)),
    
    # Hits robots[1] with damage 5
    Missile((250,800), (250,800), randint(0,360), randint(0,700)),
    
    # Hits robots[1] with damage 3
    Missile((232,777), (232,777), randint(0,360), randint(0,700)),
    
    # Hit robots[2] with damage 3 and robots[3] with damage 10 
    Missile((100,65), (100,65), randint(0,360), randint(0,700))
]

game = Game(100, robots)

def test_inflict_different_damages():
    for m in missiles:
        game._inflict_damage(m)
    
    assert robots[0].get_damage() == 20
    assert robots[1].get_damage() == 8
    assert robots[2].get_damage() == 3
    assert robots[3].get_damage() == 10


def test_inflict_no_damage():
    game._inflict_damage(
        # Current position is not the same as final position
        Missile((799,799), (500,256), randint(0,360), randint(0,700))
    )
    
    assert robots[0].get_damage() == 20
    assert robots[1].get_damage() == 8
    assert robots[2].get_damage() == 3
    assert robots[3].get_damage() == 10
