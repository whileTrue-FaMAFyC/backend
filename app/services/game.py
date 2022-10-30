import math
from typing import List

from services.Robot import Robot
from utils.services_utils import *


class Missile():
    def __init__(self, current_position, final_position, direction, remaining_distance):
        self.current_position: tuple(int, int) = current_position
        self.final_position: tuple(int, int) = final_position
        self.direction: int = direction
        self.remaining_distance: int = remaining_distance

class Game():
    def __init__(self, num_rounds: int, robots: List[Robot]):
        self.num_rounds = num_rounds
        self.robots = robots
        self._num_rounds_executed = 0
        self._missiles = []
    
    def get_rounds_remaining(self):
        return self.num_rounds - self.num_rounds_executed


    def get_robots_alive(self):
        robots_alive_acc = 0
        for r in self.robots:
            if r.get_damage() < 100:
                robots_alive_acc += 1
        return robots_alive_acc


    def _check_collisions(self, robot: Robot):
        for robot2 in self.robots:
            if robot != robot2 and robot.get_position() == robot2.get_position():
                robot._increase_damage(COLLISION_DAMAGE)


    def _inflict_damage(self, missile: Missile):
        # Missile reached its final position
        if missile.current_position == missile.final_position:
            # Check if there is any robot nearby
            for r in self.robots:
                distance = math.dist(r.get_position(), missile.current_position)
                if distance < 5:
                    r._increase_damage(10)
                elif distance < 20:
                    r._increase_damage(5)
                elif distance < 40:
                    r._increase_damage(3)
    
    
    def execute_round(self):
        if self._num_rounds_executed == self.num_rounds:
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
        for r in self.robots:
            r._attack()
            if r._missile_final_position != (None, None):
                self._missiles.append(Missile(
                    current_position=r.get_position(),
                    final_position=r._missile_final_position,
                    direction=r._cannon_direction,
                    remaining_distance=r._cannon_distance
                ))
        
        for m in self._missiles:
            self._inflict_damage(m)

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
        
        self._num_rounds_executed += 1
