
from random import randint
import math

METERS_AT_SPEED_1 = 1

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
        pass
    
    def get_velocity(self):
        pass
    
    def get_position(self):
        pass
    
    def get_damage(self):
        pass
    
    # Actions
    def _scan(self):
        pass
    
    def _shoot(self):
        pass
    
    def move(self):
        if (self._req_direction != self._direction) and self.speed < 50:
            self._direction = self._req_direction
        
        if self._previous_req_velocity == self._req_velocity:
            self._velocity = self._req_velocity
        else:
            self._velocity = math.ceil((self._velocity + self._req_velocity)/2)
        
        self._previous_req_velocity = self._req_velocity

        distance_x = math.ceil(math.cos(self._direction)*(self._velocity*METERS_AT_SPEED_1))
        distance_y = math.ceil(math.sin(self._direction)*(self._velocity*METERS_AT_SPEED_1))
        
        if (0 <= self._direction <= 90):
            new_pos_x = distance_x + self._position[0]
            new_pos_y = distance_y + self._position[1]

        if (90 < self._direction <= 180):
            new_pos_x = distance_x - self._position[0]
            new_pos_y = distance_y + self._position[1]

        if (180 < self._direction <= 270):
            new_pos_x = distance_x - self._position[0]
            new_pos_y = distance_y - self._position[1]

        if (270 < self._direction < 360):
            new_pos_x = distance_x + self._position[0]
            new_pos_y = distance_y - self._position[1]

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

        self._position[0] = new_pos_x
        self._position[1] = new_pos_y