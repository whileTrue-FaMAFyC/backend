from services.game import *
from testing.helpers.services_helpers import RobotTest

class Robot1(RobotTest):
    def initialize(self):
        pass
    
    def respond(self):
        self.drive(0, 10)

class Robot2(RobotTest):
    def initialize(self):
        pass
    
    def respond(self):
        self.drive(180,10)

class Robot3(RobotTest):
    def initialize(self):
        pass
    
    def respond(self):
        self.drive(45,10)

class Robot4(RobotTest):
    def initialize(self):
        pass
    
    def respond(self):
        pass


def test_all_rounds_executed():
    # The Robot4 does not move
    robots = [Robot1(1), Robot2(2), Robot3(3), Robot4(4)]
    game = Game(100, robots)
    for i in range(100):
        game.execute_round()
    try:
        game.execute_round()
        assert False
    except GameException as e:
        assert e.message == "All rounds already executed"
    

def test_all_robots_dead():
    robots = [Robot1(1), Robot2(2), Robot3(3)]
    for r in robots:
        r.set_damage(100)

    game = Game(100, robots)

    try:
        game.execute_round()
        assert False
    except GameException as e:
        assert e.message == "All robots dead"
        

def test_robots_move():
    # The Robot4 does not move
    robots = [Robot1(1), Robot2(2), Robot3(3), Robot4(4)]
    for r in robots:
        r.set_initial_position(499,499)

    initial_positions = [(499,499) for i in range(4)]

    game = Game(100, robots)

    game.execute_round()

    for r in range(3):
        assert robots[r].get_position() != initial_positions[r]
    assert robots[3].get_position() == initial_positions[3]


def test_check_collisions():
    robots = [Robot1(1), Robot2(2)]
    robots[0].set_initial_position(0,0)
    robots[1].set_initial_position(100,0)

    game = Game(100, robots)

    for r in range(2):
    # The damage must be 0 because the game didn't start.
        assert robots[r].get_damage() == 0

    game.execute_round()

    for r in range(2):
    # The damage must be 2 because they should have crashed.
        assert robots[r].get_damage() == 2


def test_dead_robots_go_out_of_bounds():
    # The Robot4 does not move
    robots = [Robot1(1), Robot2(2),Robot4(4)]
    # INITIAL POSITIONS
    robots[0].set_initial_position(0,0)
    robots[1].set_initial_position(100,0)
    # INITIAL DAMAGE
    robots[0].set_damage(98)
    robots[1].set_damage(98)

    game = Game(100, robots)

    game.execute_round()

    for r in range(2):
    # The damage must be 100 because they should have crashed.
        assert robots[r].get_damage() == 100

    game.execute_round()

    for r in range(2):
    # The position of both robots must be out of bounds because
    # they died the previous round.
        assert robots[r].get_position() == OUT_OF_BOUNDS
