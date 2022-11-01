from app.utils.services_utils import MISSILE_HALF_SIZE
from testing.helpers.services_helpers import RobotTest

def test_attack_500_to_700():
    robot = RobotTest(1)
    robot.set_initial_position(499,499)
    robot.cannon(0,600)
    assert robot._cannon_direction == 0
    assert robot._cannon_distance == 600
    robot._attack()
    assert robot._missile_final_position == (999-MISSILE_HALF_SIZE,499)
    assert robot._rounds_to_wait_for_cannon == 4

def test_attack_300_to_500():
    robot = RobotTest(1)
    robot.set_initial_position(499,499)
    robot.cannon(0,400)
    assert robot._cannon_direction == 0
    assert robot._cannon_distance == 400
    robot._attack()
    assert robot._missile_final_position == (899,499)
    assert robot._rounds_to_wait_for_cannon == 3

def test_attack_100_to_300():
    robot = RobotTest(1)
    robot.set_initial_position(499,499)
    robot.cannon(0,200)
    assert robot._cannon_direction == 0
    assert robot._cannon_distance == 200
    robot._attack()
    assert robot._missile_final_position == (699,499)
    assert robot._rounds_to_wait_for_cannon == 2

def test_attack_below_100():
    robot = RobotTest(1)
    robot.set_initial_position(499,499)
    robot.cannon(0,50)
    assert robot._cannon_direction == 0
    assert robot._cannon_distance == 50
    robot._attack()
    assert robot._missile_final_position == (549,499)
    assert robot._rounds_to_wait_for_cannon == 1

def test_need_to_wait_for_reload():
    robot = RobotTest(1)
    robot.set_initial_position(499,499)
    robot.cannon(0,600)
    assert robot._cannon_direction == 0
    assert robot._cannon_distance == 600
    robot._attack()
    assert robot._missile_final_position == (999-MISSILE_HALF_SIZE,499)
    assert robot._rounds_to_wait_for_cannon == 4

    robot.cannon(0,200)
    assert robot._cannon_direction == 0
    assert robot._cannon_distance == 200
    robot._attack()
    assert robot._missile_final_position == (None,None)
    assert robot._rounds_to_wait_for_cannon == 3

def test_distance_0():
    robot = RobotTest(1)
    robot.set_initial_position(499,499)
    robot.cannon(0,0)
    assert robot._cannon_direction == 0
    assert robot._cannon_distance == 0
    robot._attack()
    assert robot._missile_final_position == (None,None)
    assert robot._rounds_to_wait_for_cannon == 0