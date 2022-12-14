from fastapi import HTTPException, status
from jose import jwt
from passlib.hash import bcrypt
from pydantic import BaseModel
import smtplib
import os


SECRET_KEY = "2c329a8eca7d0c2ff68d261ad0b2e3efa66cc2603183fe6d0b4b219a11138c84"
ALGORITHM = "HS256"

SYSTEM_MAIL = "pyrobots.noreply@gmail.com"

SYSTEM_MAIL_PASSWORD = "kltrgevemdlcywkq"


EMAIL_NOT_VALID = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Email not valid."
)

AVATAR_FORMAT_NOT_VALID = HTTPException(
    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    detail="Avatar extension file not supported."
)

PASSWORD_FORMAT_NOT_VALID = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Password format not valid."
)

PASSWORD_CONFIRMATION_NOT_MATCH = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Password and password confirmation don't match."
)

INVALID_NEW_PASSWORD = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="New password is the same as the current one."
)

USERNAME_ALREADY_IN_USE = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Username already in use."
)

EMAIL_ALREADY_IN_USE = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Email already associated with another user."
)

ERROR_INSERTING_DATA = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal error when inserting the user into the database."
)

ERROR_SENDING_VERIFICATION_EMAIL = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal error sending the email with the verification code."
)

USER_NOT_REGISTERED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User not registered."
)

USER_ALREADY_VERIFIED = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User already verified."
)

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials."
)

NOT_VERIFIED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not verified user."
)

INEXISTENT_USER_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Inexistent user."
)

WRONG_VERIFICATION_CODE = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Wrong verification code."
)

ERROR_UPDATING_USER_DATA = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal error when updating the user info in the database."
)

INVALID_TOKEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid token. Not authorized."
)

AVATAR_ALREADY_LOADED = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Avatar already loaded."
)

ERROR_SENDING_RESTORE_CODE_MAIL = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal error sending the email with the password restauration code."
)

INVALID_RESTORE_CODE = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Wrong restore password code."
)

INEXISTENT_USERNAME_EMAIL_COMBINATION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="There is no user with that email and username."
)

AVATAR_NOT_INSERTED = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Avatar not inserted."
)


def is_valid_password(password):
    l, u, d = 0, 0, 0
    for i in password:
        # counting lowercase alphabets
        if (i.islower()):
            l += 1
        # counting uppercase alphabets
        if (i.isupper()):
            u += 1
        # counting digits
        if (i.isdigit()):
            d += 1

    return (l >= 1 and u >= 1 and d >= 1 and len(password) >= 8)


def send_verification_email(recipient, verification_code):
    FROM = SYSTEM_MAIL
    TO = recipient
    SUBJECT = "Here is your verification code"
    TEXT = (f"Your verification code is: {verification_code}. It is valid for 4 hours." +
            "\nDo not reply this email.")

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(SYSTEM_MAIL, SYSTEM_MAIL_PASSWORD)
        server.sendmail(FROM, TO, message)
        server.close()
        return True
    except:
        return False


def send_cleanup_email(recipient, verification_code):
    FROM = SYSTEM_MAIL
    TO = recipient
    SUBJECT = "Please signup again"
    TEXT = f"Your verification code: {verification_code} is no longer valid. Please signup again."

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(SYSTEM_MAIL, SYSTEM_MAIL_PASSWORD)
        server.sendmail(FROM, TO, message)
        server.close()
        return True
    except:
        return False


def insert_filename_to_file(file: str, filename: str):
    if file == "":
        return ""
    return "name:" + filename + ";" + file


def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.verify(plain_password, hashed_password)


class TokenData(BaseModel):
    username: str
    email: str


# Utility function to generate a token that represents 'data'
def generate_token(data: TokenData):
    data_to_encode = data.dict()
    token = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_avatar_file(avatar: str):
    if (avatar == ""):
        return "default"
    else:
        return avatar


def send_password_restore_mail(recipient, restore_code):
    FROM = SYSTEM_MAIL
    TO = recipient
    SUBJECT = "Restore your password"
    TEXT = (f"You can restore your password using this code: {restore_code}. " +
            "\nDo not reply this email.")

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(SYSTEM_MAIL, SYSTEM_MAIL_PASSWORD)
        server.sendmail(FROM, TO, message)
        server.close()
        return True
    except:
        return False
