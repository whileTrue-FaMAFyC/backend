from services.Robot import Robot

# To mock the initial position or a specific damage percentage 
class RobotTest(Robot):
    def set_initial_position(self, x, y):
        self._position = (x, y)

    def set_damage(self, damage):
        self._damage = damage
    