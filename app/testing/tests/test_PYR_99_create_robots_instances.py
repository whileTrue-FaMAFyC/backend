from testing.helpers.robot_helpers import get_robot_id_by_owner_and_name
from utils.services_utils import create_robots_instances


def test_create_robots_instances():
    robots_id = [
        get_robot_id_by_owner_and_name("tonimondejar", "CYborg34"),
        get_robot_id_by_owner_and_name("bas_benja", "pichon"),
        get_robot_id_by_owner_and_name("juliolcese", "automatax")
    ]

    robots = create_robots_instances(robots_id)
    for r in robots:
        r.initialize()

    assert robots[0].test_variable == "Soy el robot de toni"
    assert robots[1].test_variable == "Soy el robot de benja"
    assert robots[2].test_variable == "Soy el robot de juli"
