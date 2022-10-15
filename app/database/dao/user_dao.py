from pony.orm import db_session, delete
from database.models.models import User
from view_entities.user_view_entities import NewUserToDb, UserFromDb
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
        User(username=user.username, email=user.email, avatar=user.avatar,
             hashed_password=user.hashed_password, verification_code=user.verification_code,
             verified=user.verified)
        return True
    except:
        return False

@db_session
def get_user_by_username(username: str):
    return User.get(username=username) # Select from table User where column username=username.

@db_session
def get_user_by_email(email: str):
    return User.get(email=email)

@db_session
def delete_user_by_username(username: str):
    try:
        user_in_db = User.get(username=username)
        if user_in_db != None:
            user_in_db.delete()
        return True
    except:
        return False

@db_session
def delete_user_by_email(email: str):
    try:
        user_in_db = User.get(email=email)
        if user_in_db != None:
            user_in_db.delete()
        return True
    except:
        return False

@db_session
def delete_table_user():
    try:
        delete(p for p in User)
        return True
    except:
        return False

# For testing
# @db_session
# def get_users_db():
#     users = User.select()
#     return [UserFromDb.from_orm(u) for u in users]
