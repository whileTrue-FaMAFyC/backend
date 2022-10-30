from math import ceil, cos, radians, sin, degrees, atan2, sqrt
from random import randint

from utils.services_utils import *

class Robot:   
    def __init__(self, robot_id: int):
        self._id = robot_id
        self._direction: int = 0
        self._req_direction: int = 0
        self._velocity: int = 0
        self._previous_req_velocity: int = 0
        self._req_velocity: int = 0
        self._position: tuple(int, int) = (randint(0, 999), randint(0, 999))
        self._damage: int = 0
        self._cannon_direction = 0
        self._cannon_distance = 0
        self._rounds_to_wait_for_cannon = 0
        self._missile_final_position = (None,None)
        self._damage: int = 0        
        self._scan_direction: int = 0
        self._scan_resolution: int = 0
        self._scan_result: int = None

    def __eq__(self, other):
        return self._id == other._id

    # Cannon
    def is_cannon_ready(self):
        """"
        When a misil is shoot, the cannon requires a certain amount of time to
        reload. This functions is used to check if the cannon is completely
        reload.
        """
        return self._rounds_to_wait_for_cannon == 0
    
    def cannon(self, degree: int, distance: int):
        """
        This cannon prepares the cannon to shoot. If this method gets called
        more than one time, just the last one has effect. The shoot gets 
        executed at the end of the round.
        """
        if degree in range(360):
            self._cannon_direction = degree
        if distance in range(1,701):
            self._cannon_distance = distance
    
    # Scanner
    def point_scanner(self, direction, resolution_in_degrees):
        """
        With this method, the scanner gets pointed in any direction (from 0 to 
        359). The scan result will be available in the next round.
        """
        if 0 <= direction and direction <= 359:
            self._scan_direction = direction
        if 0 <= resolution_in_degrees and resolution_in_degrees <= 10:
            self._scan_resolution = resolution_in_degrees
    
    def scanned(self):
        """
        Returns the scan result from the previous round: returns the distance to
        the closest robot in the pointed direction.
        """
        return self._scan_result
    
    # Motor
    def drive(self, direction, velocity):
        """
        Establishes a new direction and velocity for the robot. If this method 
        gets called more than one time, just the last one has effect. The
        movement gets executed at the end of the round.
        """
        if (direction in range(0, 360)):
            self._req_direction = direction
            
        if (velocity in range(0, 101)):
            self._req_velocity = velocity
            
        return
    
    # Status
    def get_direction(self):
        return self._direction
    
    def get_velocity(self):
        return self._velocity

    def get_position(self):
        return self._position
    
    def get_damage(self):
        return self._damage
    
    # Actions
    def _scan(self, robots_positions):

        min_distance = MAX_POSSIBLE_DISTANCE

        min_angle = self._scan_direction - self._scan_resolution
        new_min = False

        # This is the case where the scan direction is near 0 and the resolution 
        # is such that the minimum calculated would be negative. We substract
        # 360 to get the equivalent angle in an appropiate range.
        if min_angle < 0:
            min_angle += 360
            new_min = True

        max_angle = self._scan_direction + self._scan_resolution        
        new_max = False
        
        # Same as before, but now the maximum calculated would be greater than 
        # 359, so we add 360 to get the equivalent angle in an appropiate range.
        if max_angle > 359:
            max_angle -= 360
            new_max = True

        for r in robots_positions:
            x_distance = r[0] - self._position[0]
            y_distance = r[1] - self._position[1]
            
            # tang(angle_diff) = y_distance/x_distance, so to obtain angle_diff
            # we use atan(y_distance/x_distance), atan2 allows us to take into
            # consideration the quadrant of the angle.
            angle_diff = degrees(atan2(y_distance, x_distance))
            if angle_diff < 0:
                angle_diff += 360

            distance = sqrt(pow(x_distance, 2) + pow(y_distance, 2))

            if distance < min_distance and (
               (not new_min and not new_max 
                and angle_diff >= min_angle and angle_diff <= max_angle)
               or 
               # The case where one of the limits went out of range. In this case
               # 0 will be between the valid values of angle_diff, so we can
               # consider two possibilities: angle_diff is between min_angle and
               # 360 or between 0 and max_angle. As angle_diff is between 0 and 360,
               # we can confirm that if it's greater than min_angle, it's also
               # smaller than 0, and that if it's smaller than max_angle, it's
               # also greater than 0. This is why we can use or here.               
               (new_min or new_max and
                (angle_diff >= min_angle or angle_diff <= max_angle))):
                    
                    min_distance = distance
        
        if min_distance == MAX_POSSIBLE_DISTANCE:
            self._scan_result = None
        else:
            self._scan_result = round(min_distance)

    def _attack(self):
        if self.is_cannon_ready() and self._cannon_distance > 0:
            distance_x = round_up(
                round(cos(radians(self._direction)), 5)*self._cannon_distance
            )
            distance_y = round_up(
                round(sin(radians(self._direction)), 5)*self._cannon_distance
            )

            missile_final_position_x = self._position[0] + distance_x
            missile_final_position_y = self._position[1] + distance_y

            # Check if the missile hit a wall
            if (missile_final_position_x > 999):
                missile_final_position_x = 999
            if (missile_final_position_x < 0):
                missile_final_position_x = 0
            if (missile_final_position_y > 999):
                missile_final_position_y = 999
            if (missile_final_position_y < 0):
                missile_final_position_y = 0

            self._missile_final_position = (missile_final_position_x, missile_final_position_y)

            # Set number of rounds that the user needs to wait for the cannon to reload.
            if self._cannon_distance in range(500,701):
                self._rounds_to_wait_for_cannon = ROUNDS_TO_RELOAD_CANNON_500_TO_700
            elif self._cannon_distance in range(300,500):
                self._rounds_to_wait_for_cannon = ROUNDS_TO_RELOAD_CANNON_300_TO_500
            elif self._cannon_distance in range(100, 300):
                self._rounds_to_wait_for_cannon = ROUNDS_TO_RELOAD_CANNON_100_TO_300
            else:
                self._rounds_to_wait_for_cannon = ROUNDS_TO_RELOAD_CANNON_BELOW_100

        else:
            self._rounds_to_wait_for_cannon = max(0, self._rounds_to_wait_for_cannon - 1)
            self._missile_final_position = (None,None)
    
    def _move(self):
        if (self._req_direction != self._direction) and self._velocity <= 50:
            self._direction = self._req_direction
        
        if self._previous_req_velocity == self._req_velocity:
            self._velocity = self._req_velocity
        else:
            self._velocity = ceil((self._velocity + self._req_velocity)/2)
        
        self._previous_req_velocity = self._req_velocity

        distance_x = round_up((round(cos(radians(self._direction)), 5)*self._velocity)*M_VELOC_1)
        distance_y = round_up((round(sin(radians(self._direction)), 5)*self._velocity)*M_VELOC_1)

        new_pos_x = self._position[0] + distance_x
        new_pos_y = self._position[1] + distance_y

        # Check if the robot hit a wall and do the corresponding damage
        if (new_pos_x > 999):
            new_pos_x = 999
            self._damage += 2
        if (new_pos_x < 0):
            new_pos_x = 0
            self._damage += 2
        if (new_pos_y > 999):
            new_pos_y = 999
            self._damage += 2
        if (new_pos_y < 0):
            new_pos_y = 0
            self._damage += 2

        self._position = (new_pos_x, new_pos_y)

    def _increase_damage(self, damage_to_increase: int):
        self._damage += damage_to_increase
    
