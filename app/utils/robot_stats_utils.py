from fastapi import HTTPException, status


INTERNAL_ERROR_UPDATING_ROBOT_STATS = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal error when updating the robot statistics."
)