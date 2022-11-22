from testing.helpers.services_helpers import RobotTest

r1 = RobotTest(1, 0)


def test_point_scanner():
    assert r1.get_scanner_details() == (0, 0)
    r1.point_scanner(175, 6)
    assert r1.get_scanner_details() == (175, 6)


def test_negative_resolution():
    assert r1.get_scanner_details() == (175, 6)
    r1.point_scanner(325, -1)
    assert r1.get_scanner_details() == (325, 6)


def test_resolution_more_than_10():
    assert r1.get_scanner_details() == (325, 6)
    r1.point_scanner(123, 11)
    assert r1.get_scanner_details() == (123, 6)


def test_negative_direction():
    assert r1.get_scanner_details() == (123, 6)
    r1.point_scanner(-1, 7)
    assert r1.get_scanner_details() == (123, 7)


def test_direction_more_than_359():
    assert r1.get_scanner_details() == (123, 7)
    r1.point_scanner(360, 4)
    assert r1.get_scanner_details() == (123, 4)
