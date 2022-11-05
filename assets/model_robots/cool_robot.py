class CoolRobot(Robot):
    
    def initialize(self):
        self.test_variable = "I'm CoolRobot"
        self.found_robot = False
        self.degrees = 0

    def respond(self):
        self.test_variable = "I'm CoolRobot responding"
        if not self.scanned():
            # Change scan degrees until finding someone
            self.degrees += 20 
            self.point_scanner(self.degrees, 10)
        else:
            if self.scanned() > 700:
                self.drive(self.degrees, 10)
            else:
                self.drive(self.degrees, 0)
                self.cannon(self.degrees, self.scanned())