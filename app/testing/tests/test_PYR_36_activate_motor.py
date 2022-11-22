from random import randint

from testing.helpers.services_helpers import RobotTest

test_robot = RobotTest(36, 0)


# Test with parameters OK
def test_activate_motor_ok():
    direction_ok = randint(0, 359)
    velocity_ok = randint(0, 100)

    test_robot.drive(direction_ok, velocity_ok)

    assert test_robot.get_req_direction() == direction_ok
    assert test_robot.get_req_velocity() == velocity_ok


# Test with velocity less than 0
# Velocity shouldn't change from initial test
def test_negative_velocity():
    direction = randint(0, 359)
    velocity = randint(-999, -1)

    prev_velocity = test_robot.get_req_velocity()
    test_robot.drive(direction, velocity)

    assert test_robot.get_req_direction() == direction
    assert test_robot.get_req_velocity() == prev_velocity


# Test with velocity more than 100
# Velocity shouldn'tchange from initial test
def test_velocity_more_than_100():
    direction = randint(0, 359)
    velocity = randint(101, 999)

    prev_velocity = test_robot.get_req_velocity()
    test_robot.drive(direction, velocity)

    assert test_robot.get_req_direction() == direction
    assert test_robot.get_req_velocity() == prev_velocity


# Test with direction less than 0
# Direction shouldn't change from initial test
def test_negative_direction():
    direction = randint(-999, -1)
    velocity = randint(0, 100)

    prev_direction = test_robot.get_req_direction()
    test_robot.drive(direction, velocity)

    assert test_robot.get_req_direction() == prev_direction
    assert test_robot.get_req_velocity() == velocity


# Test with direction more than 359
# Direction shouldn't change from initial test
def test_direction_more_than_359():
    direction = randint(360, 999)
    velocity = randint(0, 100)

    prev_direction = test_robot.get_req_direction()
    test_robot.drive(direction, velocity)

    assert test_robot.get_req_direction() == prev_direction
    assert test_robot.get_req_velocity() == velocity


# Both parameters wrong
def test_direction_and_velocity_wrond():
    direction = randint(360, 999)
    velocity = randint(-999, -1)

    prev_direction = test_robot.get_req_direction()
    prev_velocity = test_robot.get_req_velocity()
    test_robot.drive(direction, velocity)

    assert test_robot.get_req_direction() == prev_direction
    assert test_robot.get_req_velocity() == prev_velocity
