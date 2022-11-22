from services.match import execute_game_match
from services.simulation import execute_game_simulation
from testing.helpers.services_helpers import *


def test_timeout_match():
    robots = [
        ForeverRobotInitialize(
            1, 0), Robot2(
            2, 0), ForeverRobotRespond(
                3, 0), Robot4(
                    4, 0)]
    game = Game(1, robots)
    execute_game_match(game)

    assert robots[0].get_damage() == 100
    assert robots[1].get_damage() in [0, 2]
    assert robots[2].get_damage() == 100
    assert robots[3].get_damage() in [0, 2]


def test_timeout_simulation():
    robots = [
        ForeverRobotInitialize(
            1, 0), Robot2(
            2, 0), ForeverRobotRespond(
                3, 0), Robot4(
                    4, 0)]
    game = Game(1, robots)
    execute_game_simulation(game)

    assert robots[0].get_damage() == 100
    assert robots[1].get_damage() in [0, 2]
    assert robots[2].get_damage() == 100
    assert robots[3].get_damage() in [0, 2]
