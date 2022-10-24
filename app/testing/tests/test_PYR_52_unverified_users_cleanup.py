from datetime import datetime, timedelta
from pony.orm import db_session

from database.dao.user_dao import get_user_by_username, unverified_users_cleanup
from database.models.models import User, db

def test_unverified_users_cleanup():
    # Deletes the database
    db.drop_all_tables(with_all_data=True)
    db.create_tables()
    
    # We use a fake created time so the cleanup deletes the users.
    fake_created_time = datetime.now() - timedelta(hours=5)
    
    users = [("tonimondejar", "antoniomondejar2001@gmail.com", "Test1234",
    "fake_avatar", 123456, False), ("tonimondejar1", "antoniomondejar@gmail.com",
    "Test1234","fake_avatar", 123456, False), ("tonimondejar2", "antoniomondejar1@gmail.com",
    "Test1234","fake_avatar", 123456, False)]
    
    for username, email, password, avatar, code, verified in users:
        with db_session:
            User(username=username, email=email, hashed_password=password, avatar=avatar,
            verification_code=code, verified=verified, created_time=fake_created_time)

    for u in users:
        # Checks if the users were correctly added to the db.
        assert get_user_by_username(u[0]) != None

    unverified_users_cleanup()

    for u in users:
        # Checks if the users were correctly deleted from the db.
        assert get_user_by_username(u[0]) == None
