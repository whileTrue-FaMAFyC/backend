from services.Robot import Robot

r1 = Robot(1)
r2 = Robot(2)
r3 = Robot(3)

def test_increase_velocity():
    assert r1.get_velocity() == 0
    r1.drive(0, 80)
    r1._move()
    assert r1.get_velocity() == 40

def test_decrease_velocity():
    assert r1.get_velocity() == 40
    r1.drive(0, 20)
    r1._move()
    assert r1.get_velocity() == 30

def test_request_same_velocity():
    assert r1.get_velocity() == 30
    r1.drive(0, 20)
    r1._move()
    assert r1.get_velocity() == 20

def test_crash_wall():
    initial_damage = r1.get_damage()
    crashed = False
    while (r1.get_position()[0] <= 999 and not(crashed)):
        r1.drive(0, 100)
        r1._move()
        if r1.get_position()[0] == 999 and r1.get_damage() > initial_damage:
            crashed = True

    assert r1.get_position()[0] == 999
    assert r1.get_damage() == initial_damage + 2

def test__move_first_quadrant():
    initial_damage = r2.get_damage()
    initial_x = r2.get_position()[0]
    initial_y = r2.get_position()[1]
    r2.drive(45, 10)
    r2._move()
    assert r2.get_position()[0] > initial_x or r2.get_damage() > initial_damage
    assert r2.get_position()[1] > initial_y or r2.get_damage() > initial_damage

def test__move_second_quadrant():
    initial_damage = r2.get_damage()
    initial_x = r2.get_position()[0]
    initial_y = r2.get_position()[1]
    r2.drive(110, 10)
    r2._move()
    assert r2.get_position()[0] < initial_x or r2.get_damage() > initial_damage
    assert r2.get_position()[1] > initial_y or r2.get_damage() > initial_damage

def test__move_third_quadrant():
    initial_damage = r2.get_damage()
    initial_x = r2.get_position()[0]
    initial_y = r2.get_position()[1]
    r2.drive(235, 10)
    r2._move()
    assert r2.get_position()[0] < initial_x or r2.get_damage() > initial_damage
    assert r2.get_position()[1] < initial_y or r2.get_damage() > initial_damage

def test__move_fourth_quadrant():
    initial_damage = r2.get_damage()
    initial_x = r2.get_position()[0]
    initial_y = r2.get_position()[1]
    r2.drive(355, 10)
    r2._move()
    assert r2.get_position()[0] > initial_x or r2.get_damage() > initial_damage
    assert r2.get_position()[1] < initial_y or r2.get_damage() > initial_damage

def test_direction_change():
    assert r3.get_velocity() <= 50
    initial_direction = r3.get_direction()
    r3.drive(10, 100)
    r3._move()
    assert r3.get_direction() != initial_direction

def test_no_direction_change():
    r3.drive(10, 100)
    r3._move()
    assert r3.get_velocity() > 50
    initial_direction = r3.get_direction()
    r3.drive(50, 10)
    r3._move()
    assert r3.get_direction() == initial_direction
