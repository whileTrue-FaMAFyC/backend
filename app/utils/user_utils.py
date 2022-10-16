from fastapi import HTTPException

INVALID_TOKEN_EXCEPTION = HTTPException(
    status_code=401,
    detail="Invalid token. Not authorized."
)

INEXISTENT_USER_EXCEPTION = HTTPException(
    status_code=401,
    detail="Inexistent user"
)