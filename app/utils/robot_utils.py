from fastapi import HTTPException

BOT_NAME_EXCEPTION = HTTPException(
    status_code=409,
    detail="User already has a bot with this name."
)

ROBOT_DB_EXCEPTION = HTTPException(
    status_code=500,
    detail="Internal error when creating the new bot in the database."
)