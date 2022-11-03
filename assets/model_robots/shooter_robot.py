class ShooterRobot(Robot):
    
    def initialize(self):
        self.degrees = 0

    def response(self):
        self.cannon(self.degrees, 105)
        self.degrees += 10
        if self.degrees == 360:
            self.degrees = 0