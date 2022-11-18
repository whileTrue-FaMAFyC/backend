from datetime import datetime, timedelta
from passlib.hash import bcrypt
from pony.orm import db_session, select, delete
import schedule
import time
from threading import Thread

from database.models.models import User, RUNNING_ENVIRONMENT
from utils.user_utils import send_cleanup_email
from view_entities.user_view_entities import NewUserToDb, UserIDs


@db_session
def create_user(user: NewUserToDb):
    try:
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
    return select(u for u in User if
        (u.verified == False and
        datetime.now() - u.created_time >= timedelta(hours=4))
    )


@db_session
def get_user_avatar(username: str):
    user_avatar = User.get(username=username).avatar
    if user_avatar == "default":
        return ""
    else:
        return user_avatar


@db_session
def get_user_by_email(email: str):
    return User.get(email=email)


@db_session
def get_user_by_username(username: str):
    return User.get(username=username)


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
def update_user_avatar(username: str, avatar: str):
    try:
        User.get(username=username).set(avatar=avatar)
        return True
    except:
        return False


@db_session
def update_user_verification(username: str):
    try:
        User.get(username=username).set(verified=True)
        return True
    except:
        return False


@db_session
def update_user_password(username: str, new_password: str):
    try:
        User.get(username=username).set(
            hashed_password=bcrypt.hash(new_password)
        )
        return True
    except:
        return False


@db_session
def update_restore_password_code(username: str):
    try:
        User.get(username=username).set(restore_password_code=0)
        return True
    except:
        return False


@db_session
def delete_unverified_users():
    try:
        delete(u for u in User if
            (u.verified == False and
            datetime.now() - u.created_time >= timedelta(hours=4))
        )
        return True
    except BaseException:
        return False


@db_session
def unverified_users_cleanup():
    users = get_unverified_users()
    for u in users:
        send_cleanup_email(u.email, u.verification_code)
    delete_unverified_users()


@db_session
def get_user_by_username_and_email(username: str, email: str):
    return User.get(username=username, email=email)


@db_session
def add_password_restore_code(username: str, restore_code: int):
    try:
        User.get(username=username).set(restore_password_code=restore_code)
        return True
    except BaseException:
        return False


def schedule_unverified_users_cleanup():
    schedule.every(4).hours.do(unverified_users_cleanup)

    while True:
        schedule.run_pending()
        # Suspends execution of this thread for 100 seconds.
        time.sleep(100)
        # NOTE: The cleanup function will be running on a different thread.


@db_session
def get_user_info(username: str):
    user = User.get(username=username)

    return UserIDs(
        username=user.username,
        email=user.email
    )


# Creates a thread for cleanup unverified users every 4 hours.
if RUNNING_ENVIRONMENT == "DEPLOYMENT":
    unverified_users_cleanup_thread = Thread(target=unverified_users_cleanup)
    unverified_users_cleanup_thread.start()
