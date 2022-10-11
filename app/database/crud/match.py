from pony.orm import db_session
from database.models import Match
from schema import match

@db_session
def list_matches():
   matches = Match.select()
   return [match.ShowMatchSchema.from_orm(m) for m in matches]
