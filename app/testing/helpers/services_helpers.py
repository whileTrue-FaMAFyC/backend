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

class GameTest(Game):
    def set_missiles(self, missiles):
        self._missiles = missiles