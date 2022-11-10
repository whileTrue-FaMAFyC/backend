from utils.services_utils import *
from testing.helpers.services_helpers import RobotTest

def test_attack_500_to_700():
    robot = RobotTest(1,0)
    robot.set_initial_position(499,499)
    robot.cannon(0,600)
    assert robot._cannon_direction == 0
    assert robot._cannon_distance == 600
    robot._attack()
    assert robot._missile_final_position == (999-MISSILE_HALF_SIZE,499)
    # Because cannon distance was reduced to a number less than 500
    assert robot._rounds_to_wait_for_cannon == ROUNDS_TO_RELOAD_CANNON_300_TO_500

def test_attack_300_to_500():
    robot = RobotTest(1,0)
    robot.set_initial_position(499,499)
    robot.cannon(0,400)
    assert robot._cannon_direction == 0
    assert robot._cannon_distance == 400
    robot._attack()
    assert robot._missile_final_position == (899,499)
    assert robot._rounds_to_wait_for_cannon == ROUNDS_TO_RELOAD_CANNON_300_TO_500

def test_attack_100_to_300():
    robot = RobotTest(1,0)
    robot.set_initial_position(499,499)
    robot.cannon(0,200)
    assert robot._cannon_direction == 0
    assert robot._cannon_distance == 200
    robot._attack()
    assert robot._missile_final_position == (699,499)
    assert robot._rounds_to_wait_for_cannon == ROUNDS_TO_RELOAD_CANNON_100_TO_300

def test_attack_below_100():
    robot = RobotTest(1,0)
    robot.set_initial_position(499,499)
    robot.cannon(0,50)
    assert robot._cannon_direction == 0
    assert robot._cannon_distance == 50
    robot._attack()
    assert robot._missile_final_position == (549,499)
    assert robot._rounds_to_wait_for_cannon == ROUNDS_TO_RELOAD_CANNON_BELOW_100

def test_need_to_wait_for_reload():
    robot = RobotTest(1,0)
    robot.set_initial_position(499,499)
    robot.cannon(0,600)
    assert robot._cannon_direction == 0
    assert robot._cannon_distance == 600
    robot._attack()
    assert robot._missile_final_position == (999-MISSILE_HALF_SIZE,499)
    # Because cannon distance was reduced to a number less than 500
    assert robot._rounds_to_wait_for_cannon == ROUNDS_TO_RELOAD_CANNON_300_TO_500

    robot.cannon(0,200)
    assert robot._cannon_direction == 0
    assert robot._cannon_distance == 200
    robot._attack()
    assert robot._missile_final_position == (None,None)
    assert robot._rounds_to_wait_for_cannon == ROUNDS_TO_RELOAD_CANNON_100_TO_300

def test_distance_0():
    robot = RobotTest(1,0)
    robot.set_initial_position(499,499)
    robot.cannon(0,0)
    assert robot._cannon_direction == 0
    assert robot._cannon_distance == 0
    robot._attack()
    assert robot._missile_final_position == (None,None)
    assert robot._rounds_to_wait_for_cannon == 0

def test_missile_out_of_both_axis_bounds():
    robot = RobotTest(1,0)
    robot.set_initial_position(600,600)
    robot.cannon(45,600)
    assert robot._cannon_direction == 45
    assert robot._cannon_distance == 600
    robot._attack()
    assert robot._missile_final_position == (999-MISSILE_HALF_SIZE,999-MISSILE_HALF_SIZE)
    # Because cannon distance was reduced to a number less than 300
    assert robot._rounds_to_wait_for_cannon == ROUNDS_TO_RELOAD_CANNON_100_TO_300