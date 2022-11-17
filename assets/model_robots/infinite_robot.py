class InfiniteRobot(Robot):
    
    def initialize(self):
        self.times_called = 0

    def respond(self):
        self.times_called += 1
        if (self.times_called == 5):
            while(True):
                pass