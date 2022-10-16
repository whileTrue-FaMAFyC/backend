from services.robot import Robot

class Game():
    def __init__(self, num_rounds: int, robots: list(Robot)):
        self.num_rounds = num_rounds
        self.robots = robots
        self.num_rounds_executed = 0
    
    def robots_alive(self):
        robots_alive_acc = 0
        for r in self.robots:
            if r.life_remaining > 0:
                robots_alive_acc += 1
        return robots_alive_acc

    def execute_round(self):
        if self.num_rounds_executed == self.num_rounds:
        # You can´t execute another round. Max number of rounds executed reached
            raise Exception
        
        for r in self.robots:
            r.respond()
        for r in self.robots:
            r.scan()
        for r in self.robots:
            r.shoot()
        for r in self.robots:
            r.move()
        
        self.num_rounds_executed += 1