from services.Robot import Robot
from services.game import Game

class RobotTest(Robot):
    # To mock the initial position or a specific damage percentage
    def set_initial_position(self, x, y):
        self._position = (x, y)


    def set_damage(self, initial_damage):
        self._damage = initial_damage


    def get_req_direction(self):
        return self._req_direction


    def get_req_velocity(self):
        return self._req_velocity


    def get_scanner_details(self):
        return (self._scan_direction, self._scan_resolution)


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

class ForeverRobot(RobotTest):
    def initialize(self):
        while True:
            pass

    def respond(self):
        while True:
            pass


class GameTest(Game):
    def set_missiles(self, missiles):
        self._missiles = missiles
