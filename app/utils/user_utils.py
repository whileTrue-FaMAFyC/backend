from fastapi import HTTPException, status
from validate_email_address import validate_email
import smtplib

SYSTEM_MAIL = "pyrobots.noreply@gmail.com"
SYSTEM_MAIL_PASSWORD = "kltrgevemdlcywkq"

EMAIL_NOT_VALID = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="email not valid")

EMAIL_NOT_EXISTS = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="email does not exist")

AVATAR_FORMAT_NOT_VALID = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="avatar extension file not supported")

PASSWORD_FORMAT_NOT_VALID = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                            detail="password format not valid")

USERNAME_ALREADY_IN_USE = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                        detail="username already in use")

EMAIL_ALREADY_IN_USE = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="email already associated with another user")

ERROR_INSERTING_DATA = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="internal error when inserting the user into the database")
    
ERROR_SENDING_VERIFICATION_EMAIL = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="internal error sending the email with the verification code")

def is_valid_password(password):
    l, u, d = 0, 0, 0
    if (len(password) >= 8):
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
    
    return (l>=1 and u>=1 and d>=1 and l+u+d==len(password))


def send_verification_email(recipient, verification_code):
    FROM = SYSTEM_MAIL
    TO = recipient
    SUBJECT = "Here is your verification code"
    TEXT = f"Your verification code is: {verification_code}.\nDo not reply this email."

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        is_valid = validate_email(TO, verify=True) # Checks if the email address exists.
        print(is_valid)
        if not is_valid or is_valid == None:
            return False
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
    return "name:" + filename + ";" + file