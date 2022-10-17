from services.game import *
from testing.helpers.services_helpers import RobotTest, TestRobot

class Robot1(RobotTest):
    def initialize(self):
        pass
    
    def respond(self):
        self.drive(90, 10)

class Robot2(RobotTest):
    def initialize(self):
        pass
    
    def respond(self):
        self.drive(0,10)

class Robot3(RobotTest):
    def initialize(self):
        pass
    
    def respond(self):
        self.drive(45,10)

def test_successful_execute_round():
    robots = [Robot1(1), Robot2(2), Robot3(3)]
    game = Game(100, robots)

    robots[0].set_initial_position


def test_all_rounds_executed():
    robots = [Robot1(1), Robot2(2), Robot3(3)]
    game = Game(100, robots)
    for i in range(100):
        game.execute_round()
    try:
        game.execute_round()
    except GameException as e:
        assert e.message == "All rounds already executed"
    
    