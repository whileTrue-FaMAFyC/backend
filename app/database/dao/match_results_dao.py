from pony.orm import db_session
from typing import Dict

from database.models.models import Match, Robot, MatchResult

@db_session 
def create_match_results(match_id: int, robot_id: int, games_results: Dict[str, int]):
    try:
        games_lost = Match[match_id].num_games - games_results["games_won"] - games_results["games_tied"]
        MatchResult(
            robot=Robot[robot_id],
            match=Match[match_id],
            games_won=games_results["games_won"],
            games_tied=games_results["games_tied"],
            games_lost=games_lost
        )
        return True
    except:
        return False