from pony.orm import db_session
from database.models.models import Match 
from view_entities import robot_view_entities, match_view_entities

@db_session
def match_db_to_view(matches: Match):
    robots_view = []
    matches_view = [match_view_entities.MatchConfigView.from_orm(m) for m in matches]
    matches_and_robots = []

    for m in matches:
        robots_view.append([robot_view_entities.RobotInMatchView.from_orm(r) 
                            for r in m.robots_joined])

    for i in range(0, len(matches_view)):
        matches_and_robots.append(match_view_entities.ShowMatchView(config = matches_view[i], 
                                  robots = robots_view[i]))
    
    return matches_and_robots