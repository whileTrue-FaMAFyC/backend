from testing.helpers.services_helpers import GameTest
from services.game import Missile
game = GameTest(100, 3)


def test_advance_first_quadrant():
    game.set_missiles([Missile(0, (100, 250), (300, 450), 45, 283)])
    game._advance_missile(game._missiles[0])
    assert game._missiles[0].current_position == (118, 268)
    assert game._missiles[0].remaining_distance == 258


def test_advance_second_quadrant():
    game.set_missiles([Missile(0, (100, 250), (50, 450), 104, 206)])
    game._advance_missile(game._missiles[0])
    assert game._missiles[0].current_position == (93, 275)
    assert game._missiles[0].remaining_distance == 181


def test_advance_third_quadrant():
    game.set_missiles([Missile(0, (100, 250), (50, 150), 251, 158)])
    game._advance_missile(game._missiles[0])
    assert game._missiles[0].current_position == (91, 226)
    assert game._missiles[0].remaining_distance == 133


def test_advance_fourth_quadrant():
    game.set_missiles([Missile(0, (100, 250), (40, 10), 284, 247)])
    game._advance_missile(game._missiles[0])
    assert game._missiles[0].current_position == (107, 225)
    assert game._missiles[0].remaining_distance == 222


def test_advance_to_final_position():
    game.set_missiles([Missile(0, (100, 250), (125, 250), 0, 25)])
    game._advance_missile(game._missiles[0])
    assert game._missiles[0].current_position == (125, 250)
