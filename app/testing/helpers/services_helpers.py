from services.robot import Robot

class RobotTest(Robot):

    def set_initial_position(self, x, y):
        self._position = (x, y)

    def set_initial_damage(self, initial_damage):
        self._damage = initial_damage
    