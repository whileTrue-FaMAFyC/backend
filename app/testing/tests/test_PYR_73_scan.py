from testing.helpers.services_helpers import RobotTest
from utils.services_utils import MAX_POSSIBLE_DISTANCE

r1 = RobotTest(1)

def test_no_robots():
    r1.point_scanner(175,5)
    r1._scan([])
    assert r1.scanned() == None

def test_enemy_in_first_quadrant():
    r1.set_initial_position(400,300)
    r1.point_scanner(63,3)
    r1._scan([(600,725)])
    assert r1.scanned() == 470

def test_enemy_in_second_quadrant():
    r1.set_initial_position(1000,300)
    r1.point_scanner(145,1)
    r1._scan([(68,948)])
    assert r1.scanned() == 1135

def test_enemy_in_third_quadrant():
    r1.set_initial_position(400,400)
    r1.point_scanner(225,0)
    r1._scan([(0,0)])
    assert r1.scanned() == 566

def test_enemy_in_fourth_quadrant():
    r1.set_initial_position(400,300)
    r1.point_scanner(302,10)
    r1._scan([(409,290)])
    assert r1.scanned() == 13

def test_no_enemies_in_scan():
    r1.set_initial_position(400,300)
    r1.point_scanner(302,10)
    r1._scan([(100,100)])
    assert r1.scanned() == None

def test_many_enemies_in_scan():
    r1.set_initial_position(400,300)
    r1.point_scanner(302,10)
    r1._scan([(409,290),(406,286),(415,285)])
    assert r1.scanned() == 13

def test_negative_min_angle_range():
    r1.set_initial_position(400,300)
    r1.point_scanner(1,10)
    r1._scan([(410,299)])
    assert r1.scanned() == 10

def test_greater_than_360_max_angle_range():
    r1.set_initial_position(400,300)
    r1.point_scanner(356,10)
    r1._scan([(410,301)])
    assert r1.scanned() == 10