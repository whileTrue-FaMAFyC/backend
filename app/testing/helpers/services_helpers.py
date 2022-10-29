from services.Robot import Robot

class RobotTest(Robot):
    # To mock the initial position or a specific damage percentage 
    def set_initial_position(self, x, y):
        self._position = (x, y)

    def set_damage(self, initial_damage):
        self._damage = initial_damage
        
    def get_req_direction(self):
        return self._req_direction
    
    def get_req_velocity(self):
        return self._req_velocity
    
    def get_scanner_details(self):
        return (self._scan_direction, self._scan_resolution)