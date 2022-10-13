from pony.orm import db_session
from database.models.models import Match
from view_entities.match_view_entity import ShowMatchView

@db_session
def list_matches():
   matches = Match.select()
   print(matches)
   return matches