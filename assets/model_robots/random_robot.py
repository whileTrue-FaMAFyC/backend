
class RandomRobot(Robot):

    def initialize(self):
        pass

    def respond(self):
        import random
        self.rand_direction = random.randint(0, 359)
        self.rand_velocity = random.randint(0,100)
        self.rand_shoot_distance = random.randint(1,700)
        self.rand_shoot_direction = random.randint(0, 359)

        self.drive(self.rand_direction, self.rand_velocity)

        self.cannon(self.rand_shoot_direction, self.rand_shoot_direction)