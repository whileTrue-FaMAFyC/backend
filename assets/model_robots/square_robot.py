class SquareRobot(Robot):
    
    def initialize(self):
        self.degrees_move = 90
        self.degrees_shoot = 180
        self.moved = 0

    def respond(self):
        self.drive(self.degrees_move, 50)
        self.moved += 1
        
        if self.moved == 2:
            self.cannon(self.degrees_shoot, 100)
            self.degrees_shoot += 90
            self.degrees_move += 90
        
        
        if self.degrees_move == 360:
            self.degrees_move = 0
        
        if self.degrees_shoot == 360:
            self.degrees_shoot = 0