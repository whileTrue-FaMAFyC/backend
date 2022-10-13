from pony.orm import db_session, delete
from database.models.models import Robot

@db_session
def delete_table_robot():
    try:
        delete(p for p in Robot)
        return True
    except:
        return False