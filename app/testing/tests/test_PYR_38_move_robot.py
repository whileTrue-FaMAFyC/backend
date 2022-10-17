from services.Robot import Robot

r1 = Robot()
r2 = Robot()

def test_increase_speed():
    assert r1._velocity == 0
#    r1.drive(0, 80)
    r1.move()
    assert r1._velocity == 40

def test_decrease_speed():
    assert r1._velocity == 40
#    r1.drive(0, 20)
    r1.move()
    assert r1._velocity == 30

def test_request_same_speed():
    assert r1._velocity == 30
#    r1.drive(0, 20)
    r1.move()
    assert r1._velocity == 20

def test_crash_wall():
    initial_damage = r1._damage
    while (r1._position[0] <= 999):
#        r1.drive(0, 100)
        r1.move()
    assert r1._position[0] == 999
    assert r1._damage == initial_damage + 2

def test_move_first_quadrant():
    initial_x = r2._position[0]
    initial_y = r2._position[1]
#    r2.drive(45, 10)
    r2.move()
    assert r2._position[0] > initial_x
    assert r2._position[1] > initial_y

def test_move_second_quadrant():
    initial_x = r2._position[0]
    initial_y = r2._position[1]
#    r2.drive(110, 10)
    r2.move()
    assert r2._position[0] < initial_x
    assert r2._position[1] > initial_y


def test_move_third_quadrant():
    initial_x = r2._position[0]
    initial_y = r2._position[1]
#    r2.drive(235, 10)
    r2.move()
    assert r2._position[0] < initial_x
    assert r2._position[1] < initial_y

def test_move_fourth_quadrant():
    initial_x = r2._position[0]
    initial_y = r2._position[1]
#    r2.drive(355, 10)
    r2.move()
    assert r2._position[0] > initial_x
    assert r2._position[1] < initial_y