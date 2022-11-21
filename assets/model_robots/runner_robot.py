class RunnerRobot(Robot):
    
    def initialize(self):
        self.reached_wall = False
        self.degrees = 90
        self.velocity = 50

    def respond(self):
        if not self.reached_wall:
            self.drive(0, self.velocity)
            if self.get_position()[0] == 983:
                self.velocity = 50
                self.reached_wall = True
        else:
            if self.near_corner():
                self.degrees += 90
                if self.degrees == 360:
                    self.degrees = 0
                self.velocity = 50
            self.drive(self.degrees, self.velocity)
    
    def near_corner(self):
        x, y = self.get_position()
        return (((x + 35 >= 983) and (y + 35 >= 983))
             or ((x + 35 >= 983) and (y - 35 <= 16))
             or ((x - 35 <= 16) and (y + 35 >= 983)) 
             or ((x - 35 <= 16) and (y - 35 <= 16)))