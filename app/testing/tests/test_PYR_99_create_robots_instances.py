from testing.helpers.robot_helpers import get_robot_id_by_owner_and_name
from utils.services_utils import create_robots_instances


def test_create_robots_instances():
    robots_id = [
        get_robot_id_by_owner_and_name("tonimondejar", "CYborg34"),
        get_robot_id_by_owner_and_name("bas_benja", "Bumblebee"),
        get_robot_id_by_owner_and_name("juliolcese", "automatax")
    ]

    robots = create_robots_instances(robots_id)
    for r in robots:
        r.initialize()

    assert robots[0].test_variable == "I'm " + type(robots[0]).__name__
    assert robots[1].test_variable == "I'm " + type(robots[1]).__name__
    assert robots[2].test_variable == "I'm " + type(robots[2]).__name__
    
    for r in robots:
        r.respond()
        
    assert robots[0].test_variable == "I'm " + type(robots[0]).__name__ + " responding"
    assert robots[1].test_variable == "I'm " + type(robots[1]).__name__ + " responding"
    assert robots[2].test_variable == "I'm " + type(robots[2]).__name__ + " responding"
