class ShooterRobot(Robot):
    
    def initialize(self):
        self.test_variable = "I'm ShooterRobot"
        self.degrees = 0

    def respond(self):
        self.test_variable = "I'm ShooterRobot responding"
        self.cannon(self.degrees, 105)
        self.degrees += 10