from datetime import datetime, timedelta
from threading import Thread
from pony.orm import db_session, select, delete
import schedule, time

from database.models.models import User, RUNNING_ENVIRONMENT
from utils.user_utils import send_cleanup_email,  get_b64_from_path
from view_entities.user_view_entities import NewUserToDb

#
# The db_session() decorator performs the following actions on exiting function:
#
#  - Performs rollback of transaction if the function raises an exception
#  - Commits transaction if data was changed and no exceptions occurred
#  - Returns the database connection to the connection pool
#  - Clears the database session cache
#

# Instances of class User created within a function are added to the database as
#  a row of table 'User' when exiting.

@db_session
def create_user(user: NewUserToDb):
    try:
        # Inserts parameter user in to the 'User' table
        User(
            username=user.username, 
            email=user.email, 
            avatar=user.avatar,
            hashed_password=user.hashed_password, 
            verification_code=user.verification_code,
            verified=user.verified
        )
        return True
    except:
        return False


@db_session
def get_unverified_users():
    return select(u for u in User if (u.verified == False and
                    datetime.now()-u.created_time >= timedelta(hours=4)))


@db_session
def get_user_avatar(username: str):
    user_avatar = User.get(username=username).avatar
    if user_avatar == "default":
        return ""
    else:
        return get_b64_from_path(user_avatar)


@db_session
def get_user_by_email(email: str):
    return User.get(email=email)


@db_session
def get_user_by_username(username: str):
    return User.get(username=username) # Select from table User where column username=username.


@db_session
def get_user_by_username_or_email(username_or_email: str):
    user = get_user_by_username(username_or_email)
    if not user:
        user = get_user_by_email(username_or_email)
    return user


@db_session
def get_usernames():
    return select(u.username for u in User)


@db_session
def update_user_avatar(username: str, avatar_path: str):
    try:
        User.get(username=username).set(avatar=avatar_path)
        return True
    except:
        return False


@db_session
def update_user_verification(username: str):
    try:
        user_db = User.get(username=username)
        user_db.set(verified=True)
        return True
    except:
        return False


@db_session
def delete_unverified_users():
    try:
        delete(u for u in User if (u.verified == False and
                    datetime.now()-u.created_time >= timedelta(hours=4)))
        return True
    except:
        return False


@db_session
def unverified_users_cleanup():
    users = get_unverified_users()
    for u in users:
        send_cleanup_email(u.email, u.verification_code)
    delete_unverified_users()


def schedule_unverified_users_cleanup():
    schedule.every(4).hours.do(unverified_users_cleanup)

    while True:
        schedule.run_pending()
        # Suspends execution of this thread for 100 seconds.
        time.sleep(100)
        # NOTE: The cleanup function will be running on a different thread.

# Creates a thread for cleanup unverified users every 4 hours.
if RUNNING_ENVIRONMENT == "DEPLOYMENT":
    unverified_users_cleanup_thread = Thread(target=unverified_users_cleanup)
    unverified_users_cleanup_thread.start()