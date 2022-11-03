class ShooterRobot(Robot):
    
    def initialize(self):
        self.degrees = 0

    def respond(self):
        self.cannon(self.degrees, 105)
        self.degrees += 10