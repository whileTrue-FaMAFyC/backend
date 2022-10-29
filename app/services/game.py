from utils.services_utils import *

class Game():
    def __init__(self, num_rounds: int, robots: list):
        self.num_rounds = num_rounds
        self.robots = robots
        self.num_rounds_executed = 0
    
    def get_rounds_remaining(self):
        return self.num_rounds - self.num_rounds_executed

    def get_robots_alive(self):
        robots_alive_acc = 0
        for r in self.robots:
            if r.get_damage() < 100:
                robots_alive_acc += 1
        return robots_alive_acc

    def _check_collisions(self, robot):
        for robot2 in self.robots:
            if robot != robot2 and robot.get_position() == robot2.get_position():
                robot._increase_damage(COLLISION_DAMAGE)

    def execute_round(self):
        if self.num_rounds_executed == self.num_rounds:
        # You can´t execute another round. Max number of rounds executed reached
            raise GameException(detail="All rounds already executed")

        if self.get_robots_alive() == 0:
        # You can´t execute another round. All robots dead.
            raise GameException(detail="All robots dead")

        for r in self.robots:
            r.respond()

        # TO DO
        for r in self.robots:
            others_positions = []

            for other_r in self.robots:
                if not other_r == r:
                    others_positions.append(other_r.get_position)

            r._scan(others_positions)
            
        # for r in self.robots:
        #     r.shoot()
        # self.update_damage()

        for r in self.robots:
        # Check if the robot got killed during the shooting stage
            if r.get_damage() < 100:
                r._move()

        for r in self.robots:
            if r.get_damage() >= 100:
                r._position = OUT_OF_BOUNDS

        for r in self.robots:
        # Check if the robot got killed during the moving stage 
        # (collision with the walls damage)
            if r.get_damage() < 100:
                self._check_collisions(r)
        
        self.num_rounds_executed += 1