import smtplib
from validate_email import validate_email

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

SYSTEM_MAIL = "pyrobots.noreply@gmail.com"
SYSTEM_MAIL_PASSWORD = "kltrgevemdlcywkq"

def send_verification_email(recipient, verification_code):
    FROM = SYSTEM_MAIL
    TO = recipient
    SUBJECT = "Here is your verification code"
    TEXT = f"Your verification code is: {verification_code}.\nDo not reply this email."

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        is_valid = validate_email(TO) # Checks if the email address exists.
        if not is_valid:
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
