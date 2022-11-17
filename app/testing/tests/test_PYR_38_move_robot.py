from utils.services_utils import ROBOT_HALF_SIZE
from testing.helpers.services_helpers import RobotTest

r1 = RobotTest(1,0)
r2 = RobotTest(2,0)
r3 = RobotTest(3,0)
r4 = RobotTest(4,0)

def test_increase_velocity():
    assert r1.get_velocity() == 0
    r1.drive(0, 80)
    r1._move()
    assert r1.get_velocity() == 27 # (80-0)/3 

def test_decrease_velocity():
    assert r1.get_velocity() == 27
    r1.drive(0, 20)
    r1._move()
    assert r1.get_velocity() ==  25 # (27-0)/3 

def test_stop_motor():
    while r1.get_velocity() > 10:
        r1.drive(0, 7)
        r1._move()
    r1.drive(0, 0)
    r1._move()
    assert r1.get_velocity() == 0

def test_max_velocity():
    while r1.get_velocity() < 90:
        r1.drive(0, 95)
        r1._move()
    r1.drive(0, 100)
    r1._move()
    assert r1.get_velocity() == 100

def test_crash_wall():
    initial_damage = r1.get_damage()
    crashed = False
    while (r1.get_position()[0] <= 999 and not(crashed)):
        r1.drive(0, 100)
        r1._move()
        if r1.get_position()[0] == 999 - ROBOT_HALF_SIZE and r1.get_damage() > initial_damage:
            crashed = True

    assert r1.get_position()[0] == 999 - ROBOT_HALF_SIZE
    assert r1.get_damage() == initial_damage + 2

def test_180_degrees():
    r4.set_initial_position(983, 983)
    while r4.get_position() != (16, 983):
        r4.drive(180,50)
        r4._move()
        assert r4.get_position()[1] == 983
    
    assert r4.get_position() == (16, 983)

def test_move_first_quadrant():
    initial_damage = r2.get_damage()
    initial_x = r2.get_position()[0]
    initial_y = r2.get_position()[1]
    r2.drive(45, 10)
    r2._move()
    assert r2.get_position()[0] > initial_x or r2.get_damage() > initial_damage
    assert r2.get_position()[1] > initial_y or r2.get_damage() > initial_damage

def test_move_second_quadrant():
    initial_damage = r2.get_damage()
    initial_x = r2.get_position()[0]
    initial_y = r2.get_position()[1]
    r2.drive(110, 10)
    r2._move()
    assert r2.get_position()[0] < initial_x or r2.get_damage() > initial_damage
    assert r2.get_position()[1] > initial_y or r2.get_damage() > initial_damage

def test_move_third_quadrant():
    initial_damage = r2.get_damage()
    initial_x = r2.get_position()[0]
    initial_y = r2.get_position()[1]
    r2.drive(235, 10)
    r2._move()
    assert r2.get_position()[0] < initial_x or r2.get_damage() > initial_damage
    assert r2.get_position()[1] < initial_y or r2.get_damage() > initial_damage

def test_move_fourth_quadrant():
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
