from database.models.models import Match 
from pony.orm import db_session
from view_entities.match_view_entities import *
from view_entities.robot_view_entities import *

# Transforms the matches selected from the database to the format that will be
# sent to the frontend.
@db_session
def match_db_to_view(matches: Match):
    for m in matches:
        print(m)
    matches_info = [MatchInfo.from_orm(m) for m in matches]
    all_robots_joined = []
    info_and_robots = []

    for m in matches:
       all_robots_joined.append(len(m.robots_joined))

    for i in range(0, len(matches_info)):
        # info_and_robots.append(ShowMatch(match_info = matches_info[i],
        #                        robots_joined = all_robots_joined[i]))
        info_and_robots.append(
            ShowMatch(match_id = matches_info[i].match_id,
                      name = matches_info[i].name,
                      creator_user = matches_info[i].creator_user,
                      max_players = matches_info[i].max_players,
                      robots_joined = all_robots_joined[i]))

    return info_and_robots