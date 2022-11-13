from pony.orm import db_session

from database.dao.robot_dao import get_bot_by_id
from database.models.models import Robot, RobotStats


@db_session
def update_robot_stats(
    robot_id: int, 
    is_winner: bool, 
    is_tier: bool,
    is_loser: bool,
    games_win_proportion: float
):
    robot: Robot = get_bot_by_id(robot_id)
    robot_stats: RobotStats = RobotStats.get(robot=robot)
    
    current_matches_played = robot_stats.matches_played
    current_matches_won = robot_stats.matches_won
    current_matches_tied = robot_stats.matches_tied
    current_matches_lost = robot_stats.matches_lost
    current_games_win_rate = robot_stats.games_win_rate
    
    try:  
        robot_stats.set(
            matches_played=
                current_matches_played+1,
            matches_won=
                (current_matches_won+1) if is_winner else current_matches_won,
            matches_tied=
                (current_matches_tied+1) if is_tier else current_matches_tied,
            matches_lost=
                (current_matches_lost+1) if is_loser else current_matches_lost,
            games_win_rate=
                (current_games_win_rate+games_win_proportion)/2 
                if current_games_win_rate != 0 else games_win_proportion
        )        
        return True
    except: 
        return False
