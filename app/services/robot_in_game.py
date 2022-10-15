from random import randint, randchoice
import math

class Robot:
    def __init__(self):
        self.position_x = randint(0,999)
        self.position_y = randint(0,999)
        self.speed = 0
        self.previous_speed
        self.direction = randchoice([0, 90, 180, 270])
        self.damage = 0
    
    def move(self, new_dir, new_speed):
        if (dir != self.dir) and self.speed < 50:
            self.dir = new_dir
        if self.previous_speed == new_speed:
            self.speed = new_speed
        else:
            self.speed = math.ceil(abs(self.speed - new_speed))/2
        distance = self.speed
        new_position_x = math.ceil(math.cos(self.direction)*distance)
        new_position_y = math.ceil(math.sin(self.direction)*distance)
        if (new_position_x > 999):
            new_position_x = 999
            self.damage += 2
        if (new_position_x < 0):
            new_position_x = 0
            self.damage += 2
        if (new_position_y > 999):
            new_position_y = 999
            self.damage += 2
        if (new_position_y < 0):
            new_position_y = 0
            self.damage += 2
        self.position_x = new_position_x
        self.position_y = new_position_y


