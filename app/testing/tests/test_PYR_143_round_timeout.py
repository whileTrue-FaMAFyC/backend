from services.game import *
from testing.helpers.services_helpers import *

def test_timeout():
    robots = [ForeverRobot(1,0), Robot2(2,0), ForeverRobot(3,0), Robot4(4,0)]
    game = Game(100, robots)

    game.execute_round()

    assert robots[0].get_damage() == 100
    assert robots[1].get_damage() == 0
    assert robots[2].get_damage() == 100
    assert robots[3].get_damage() == 0
