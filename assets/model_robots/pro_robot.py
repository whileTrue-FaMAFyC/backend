class ProRobot(Robot):
    def initialize(self):
        self.shoot = 0
        self.move = 180
        self.scan = 0
        self.enemies_right = False
        self.enemies_left = False
        self.enemies_up = False
        self.enemies_down = False
    
    def respond(self):
        if self.enemies_right:
            self.shoot = 0
            self.move = 180
        elif self.enemies_left:
            self.shoot = 180
            self.move = 0
        elif self.enemies_up:
            self.shoot = 90
            self.move = 270
        else:
            self.shoot = 270
            self.move = 90

        self.point_scanner(self.scan, 10)

        if self.scanned() != None:
            if self.scan == 0:
                self.enemies_right = True
            elif self.scan == 90:
                self.enemies_up = True
            elif self.scan == 180:
                self.enemies_left = True
            else:
                self.enemies_down = True
        
        self.drive(self.move, 50)
        self.cannon(self.shoot, 200)
        self.scan += 90
        if self.scan == 360:
            self.scan = 0
