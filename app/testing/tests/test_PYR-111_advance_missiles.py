from testing.helpers.services_helpers import GameTest
from services.game import Missile
game = GameTest(100, 3)

def test_advance_first_quadrant():
    game.set_missiles([Missile((100,250), (300, 450), 45, 283)])
    game._advance_missile(game._missiles[0])
    assert game._missiles[0].current_position == (171, 321)
    assert game._missiles[0].remaining_distance == 183

def test_advance_second_quadrant():
    game.set_missiles([Missile((100,250), (50, 450), 104, 206)])
    game._advance_missile(game._missiles[0])
    assert game._missiles[0].current_position == (75, 348)
    assert game._missiles[0].remaining_distance == 106

def test_advance_third_quadrant():
    game.set_missiles([Missile((100,250), (50, 150), 251, 158)])
    game._advance_missile(game._missiles[0])
    assert game._missiles[0].current_position == (67, 155)
    assert game._missiles[0].remaining_distance == 58

def test_advance_fourth_quadrant():
    game.set_missiles([Missile((100,250), (40, 10), 284, 247)])
    game._advance_missile(game._missiles[0])
    assert game._missiles[0].current_position == (125, 152)
    assert game._missiles[0].remaining_distance == 147

def test_advance_to_final_position():
    game.set_missiles([Missile((100,250), (140, 290), 45, 57)])
    game._advance_missile(game._missiles[0])
    assert game._missiles[0].current_position == (140, 290)