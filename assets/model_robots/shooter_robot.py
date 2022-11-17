class ShooterRobot(Robot):
    
    def initialize(self):
        self.degrees = 0

    def respond(self):
        self.point_scanner(self.degrees, 10)
        if self.scanned() != None:
            self.cannon(self.degrees, self.scanned())
        else:
            self.degrees += 10