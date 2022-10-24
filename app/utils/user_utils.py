from datetime import datetime, timedelta
from fastapi import HTTPException, status
from jose import jwt
from passlib.hash import bcrypt
from pydantic import BaseModel
import smtplib


SECRET_KEY = "2c329a8eca7d0c2ff68d261ad0b2e3efa66cc2603183fe6d0b4b219a11138c84"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440 # One day

SYSTEM_MAIL = "pyrobots.noreply@gmail.com"

SYSTEM_MAIL_PASSWORD = "kltrgevemdlcywkq"

EMAIL_NOT_VALID = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="email not valid")

AVATAR_FORMAT_NOT_VALID = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="avatar extension file not supported")

PASSWORD_FORMAT_NOT_VALID = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="password format not valid")

USERNAME_ALREADY_IN_USE = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="username already in use")

EMAIL_ALREADY_IN_USE = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="email already associated with another user")

ERROR_INSERTING_DATA = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="internal error when inserting the user into the database")
    
ERROR_SENDING_VERIFICATION_EMAIL = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="internal error sending the email with the verification code")

USER_NOT_REGISTERED = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="user not registered")

USER_ALREADY_VERIFIED = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="user already verified")

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="invalid credentials"
)

NOT_VERIFIED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="not verified user"
)

INEXISTENT_USER_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="inexistent user"
)

WRONG_VERIFICATION_CODE = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="wrong verification code")

ERROR_UPDATING_USER_DATA = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="internal error when updating the user info in the database")

INVALID_TOKEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid token. Not authorized."
)


def is_valid_password(password):
    l, u, d = 0, 0, 0
    for i in password:
        # counting lowercase alphabets
        if (i.islower()):
            l+=1 
        # counting uppercase alphabets
        if (i.isupper()):
            u+=1
        # counting digits
        if (i.isdigit()):
            d+=1

    return (l>=1 and u>=1 and d>=1 and len(password)>=8)


def send_verification_email(recipient, verification_code):
    FROM = SYSTEM_MAIL
    TO = recipient
    SUBJECT = "Here is your verification code"
    TEXT = f"Your verification code is: {verification_code}.\nDo not reply this email."

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


# Utility function to generate a token that representes 'data'
def generate_token(data: TokenData):
    data_to_encode = data.dict()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp": expire})
    token = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token