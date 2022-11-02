class RunningRobot(Robot):
    
    def initialize(self):
        self.corners = [(16,16), (16,983), (983,16), (983,983)]
        self.reached_wall = False
        self.degrees = 270

    def respond(self):
        if self.reached_wall == False:
            self.drive(0, 50)
            if self.get_position()[0] == 983:
                self.reached_wall = True
        else:
            self.drive(self.degrees, 50)
            if self.get_position() in self.corners:
                self.degrees += 90
                if self.degrees == 360:
                    self.degrees = 0
