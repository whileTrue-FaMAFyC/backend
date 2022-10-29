from math import ceil, cos, radians, sin, degrees, atan
from random import randint

from utils.services_utils import round_up, M_VELOC_1

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
        self._scan_angle: int = 0
        self._scan_resolution: int = 0

    def __eq__(self, other):
        return self._id == other._id

    # Cannon
    def is_cannon_ready(self):
        """"
        When a misil is shoot, the cannon requires a certain amount of time to
        reload. This functions is used to check if the cannon is completely
        reload.
        """
        pass
    
    def cannon(self, degree: int, distance: int):
        """
        This cannon prepares the cannon to shoot. If this method gets called
        more than one time, just the last one has effect. The shoot gets 
        executed at the end of the round.
        """
        pass
    
    # Scanner
    def point_scanner(self, direction, resolution_in_degrees):
        """
        With this method, the scanner gets pointed in any direction (from 0 to 
        359). The scan result will be available in the next round.
        """
        pass
    
    def scanned(self):
        """
        Returns the scan result from the previous round: returns the distance to
        the closes robot in the pointed direction.
        """
        pass
    
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
    def _scan(self, robots):

        # The maximum possible distance between two robots is 1414 meters
        # sqrt(1000^2 + 1000^2) = 1414,21
        min_distance = 1415
        min_angle = self._scan_angle - self._scan_resolution
        max_angle = self._scan_angle + self._scan_resolution        
        
        for r in robots:
            x_distance = abs(r[0] - self._position[0])
            y_distance = abs(r[1] - self._position[1])
            angle_difference = degrees(atan(x_distance/y_distance))

            if (min_angle <= angle_difference or angle_difference <= max_angle):
                min_distance = sin(radians(angle_difference))*x_distance

        return min_distance
    
    def _shoot(self):
        pass
    
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

    # Is called when two bots crash
    def _increase_damage(self, damage_to_increase: int):
        self._damage += damage_to_increase