class CoolRobot(Robot):

    def initialize(self):
        self.found_robot = False
        self.degrees = 0

    def respond(self):
        if not self.scanned():
            # Change scan degrees until finding someone
            self.degrees += 3
            self.point_scanner(self.degrees, 2)
        else:
            if self.scanned() > 700:
                self.drive(self.degrees, 100)
            else:
                self.drive(self.degrees, 0)
                self.cannon(self.degrees, self.scanned())