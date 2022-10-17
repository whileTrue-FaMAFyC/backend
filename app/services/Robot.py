
from random import randint

class Robot:   
    def __init__(self, robot_id: int):
        self._id = robot_id
        self._direction: int = 0
        self._velocity: int = 0
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
        pass
    
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
    
    def _move(self):
        pass
 