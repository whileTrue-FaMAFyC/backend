import email_validator
from utils.user_utils import *
from database.dao.user_dao import *

# Returns True if the email format is valid
def validate_email_format(email):
    try:
        # Checks the syntax of the email. Needs the email_validator module prefix for issues
        #  with another function of utils/user.py.
        v = email_validator.validate_email(email)
        return True
    except email_validator.EmailNotValidError as e:
        return False

def validate_password(password):
    return is_valid_password(password)

# Returns True if the username is not in use
def validate_username_not_in_use(username):
    return get_user_by_username(username) is None

# Returns True if the email is not in use
def validate_email_not_in_use(email):
    return get_user_by_email(email) is None
