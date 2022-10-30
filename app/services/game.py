from utils.services_utils import *
from math import cos, sin, radians

class Missile():
    def __init__ (self, current_position, final_position, direction, remaining_distance):
        self.current_position = current_position
        self.final_position = final_position
        self.direction = direction
        self.remaining_distance = remaining_distance

class Game():
    def __init__(self, num_rounds: int, robots: list):
        self.num_rounds = num_rounds
        self.robots = robots
        self.num_rounds_executed = 0
        self._missiles = [Missile]
    
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

    def _advance_missile(self, missile: Missile):
        if missile.remaining_distance <= MISSILE_ADVANCE:
            missile.current_position = missile.final_position

        else:
            missile.current_position = (
                missile.current_position[0] + 
                round_up(round(cos(radians(missile.direction)), 5)*MISSILE_ADVANCE), 
                missile.current_position[1] + 
                round_up(round(sin(radians(missile.direction)), 5)*MISSILE_ADVANCE)
            )

        missile.remaining_distance -= MISSILE_ADVANCE

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
        # for r in self.robots:
        #     r.scan()
        # for r in self.robots:
        #     r.shoot()
        # self.update_damage()

        for m in self._missiles:
            self._advance_missile(m)
        
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