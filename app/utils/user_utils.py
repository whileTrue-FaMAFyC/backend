from fastapi import HTTPException, status

USER_NOT_REGISTERED = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="user not registered")

USER_ALREADY_VERIFIED = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="user already verified")

WRONG_VERIFICATION_CODE = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="wrong verification code")

ERROR_UPDATING_USER_DATA = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="internal error when updating the user info in the database")