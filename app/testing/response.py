from itertools import permutations

basbenja_r1 = {"owner": {"username": "basbenja"}, "name": "robot1"}
basbenja_r2 = {"owner": {"username": "basbenja"}, "name": "robot2"}
jolcese_r1 = {"owner": {"username": "jolcese"}, "name": "robot1"}
tonimond_r3 = {"owner": {"username": "tonimond"}, "name": "robot3"}
match1_rob = [basbenja_r1, jolcese_r1]
match1_pos_comb = [list(p) for p in permutations(match1_rob)]
matchexc_rob = [basbenja_r2, jolcese_r1, tonimond_r3]
matchexc_pos_comb = [list(p) for p in permutations(matchexc_rob)]
robots_order = [list(m1 + me) for m1 in match1_pos_comb for me in matchexc_pos_comb]

def base_response(robots):
  return (
  [{"config": {"name": "match1", "creator_user": {"username": "basbenja"}, 
  "min_players": 2, "max_players": 4, "num_games": 10, "num_rounds": 1570}, 
  "robots": [robots[0], robots[1]]}, 
  {"config": {"name": "match2", "creator_user": {"username": "basbenja"}, 
  "min_players": 3, "max_players": 3, "num_games": 200, "num_rounds": 100000}, 
  "robots": [{"owner": {"username": "basbenja"}, "name": "robot2"}]}, 
  {"config": {"name": "match1", "creator_user": {"username": "jolcese"}, 
  "min_players": 2, "max_players": 3, "num_games": 1, "num_rounds": 1}, 
  "robots": [{"owner": {"username": "jolcese"}, "name": "robot1"}]}, 
  {"config": {"name": "jmatch2", "creator_user": {"username": "jolcese"}, 
  "min_players": 2, "max_players": 3, "num_games": 1, "num_rounds": 1}, 
  "robots": [{"owner": {"username": "jolcese"}, "name": "robot1"}]}, 
  {"config": {"name": "24601", "creator_user": {"username": "tonimond"}, 
  "min_players": 2, "max_players": 2, "num_games": 157, "num_rounds": 3250}, 
  "robots": [{"owner": {"username": "tonimond"}, "name": "robot1"}]}, 
  {"config": {"name": "match!", "creator_user": {"username": "tonimond"}, 
  "min_players": 4, "max_players": 4, "num_games": 200, "num_rounds": 1}, 
  "robots": [robots[2], robots[3], robots[4]]}]
)
 
possible_responses = [base_response(i) for i in robots_order]