from func_timeout import func_timeout, FunctionTimedOut
from math import cos, sin, radians, dist
from typing import List, Tuple

from services.Robot import Robot
from utils.services_utils import *


class Missile():
    def __init__(self, id,  current_position, final_position, direction, remaining_distance):
        self.id = id
        self.initial_position = current_position
        self.current_position: Tuple(int, int) = current_position
        self.final_position: Tuple(int, int) = final_position
        self.direction: int = direction
        self.remaining_distance: int = remaining_distance


class Game():
    def __init__(self, num_rounds: int, robots: List[Robot]):
        self.num_rounds = num_rounds
        self.robots = robots
        self._num_rounds_executed = 0
        self._missiles = []
        self._missile_id = 0

    def get_rounds_remaining(self):
        return self.num_rounds - self._num_rounds_executed


    def get_robots_alive(self):
        robots_alive_acc = 0
        for r in self.robots:
            if r.get_damage() < 100:
                robots_alive_acc += 1
        return robots_alive_acc


    def _check_collisions(self, robot: Robot):
        for robot2 in self.robots:
            vertexs = get_vertex(tuple(robot2.get_position()))
            if robot != robot2 and is_inside(vertexs, robot.get_position()):
                robot._increase_damage(COLLISION_DAMAGE)


    def _advance_missile(self, missile: Missile):
        if missile.remaining_distance <= MISSILE_ADVANCE+5:
            missile.current_position = missile.final_position

        else:
            missile.current_position = tuple((
                missile.current_position[0] + round_up(round(cos(radians(missile.direction)),5)*MISSILE_ADVANCE), 
                missile.current_position[1] + round_up(round(sin(radians(missile.direction)),5)*MISSILE_ADVANCE)
            ))
        # print(missile.current_position, missile.id, missile.direction)
        missile.remaining_distance = max(0,missile.remaining_distance-MISSILE_ADVANCE)


    def _inflict_damage(self, missile: Missile):
        # Missile reached its final position
        if missile.current_position == missile.final_position:
            # Check if there is any robot nearby
            for r in self.robots:
                distance = dist(r.get_position(), missile.current_position)
                if distance < DISTANCE_DAMAGE_10:
                    r._increase_damage(10)
                elif distance < DISTANCE_DAMAGE_5:
                    r._increase_damage(5)
                elif distance < DISTANCE_DAMAGE_3:
                    r._increase_damage(3)


    def execute_round(self):
        if self._num_rounds_executed == self.num_rounds:
        # You can´t execute another round. Max number of rounds executed reached
            raise GameException(detail="All rounds already executed")

        if self.get_robots_alive() == 0:
        # You can´t execute another round. All robots dead.
            raise GameException(detail="All robots dead")

        for m in self._missiles:
            if m.current_position == m.final_position:
                self._missiles.remove(m)

        for r in self.robots:
            if r.get_damage() < 100:
                try:
                    func_timeout(timeout=RESPOND_TIMEOUT, func=r.respond)
                except:
                    # print('Robot timed out during respond!')
                    r._increase_damage(100)

        for r in self.robots:
            others_positions = []

            for other_r in self.robots:
                if other_r != r and other_r.get_damage() < 100:
                    if other_r.get_position() != OUT_OF_BOUNDS:
                        others_positions.append(other_r.get_position())

            if r.get_damage() < 100:
                r._scan(others_positions)

        for r in self.robots:
            if r.get_damage() < 100:
                r._attack()
                if r._missile_final_position != (None, None):
                    self._missiles.append(Missile(
                        id=self._missile_id,
                        current_position=r.get_position(),
                        final_position=r._missile_final_position,
                        direction=r._cannon_direction,
                        remaining_distance=r._cannon_distance
                    ))
                    self._missile_id += 1

        for m in self._missiles:
            self._advance_missile(m)

        for m in self._missiles:
            self._inflict_damage(m)

        for r in self.robots:
        # Check if the robot got killed during the shooting stage
            if r.get_damage() < 100:
                r._move()

        for r in self.robots:
            if r.get_damage() >= 100:
                r._final_position = r.get_position()
                r._position = OUT_OF_BOUNDS

        for r in self.robots:
        # Check if the robot got killed during the moving stage
        # (collision with the walls damage)
            if r.get_damage() < 100:
                self._check_collisions(r)

        self._num_rounds_executed += 1