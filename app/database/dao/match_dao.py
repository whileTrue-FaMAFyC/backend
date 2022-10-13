from pony.orm import db_session, delete
from database.models.models import Match

@db_session
def delete_table_match():
    try:
        delete(p for p in Match)
        return True
    except:
        return False