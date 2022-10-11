from pony.orm import db_session
from database.models import Match
from schema import match

@db_session
def get_matches():
   matches = Match.select().prefetch(Match.robots_joined)
   return [match.ShowMatchSchema.from_orm(m) for m in matches]