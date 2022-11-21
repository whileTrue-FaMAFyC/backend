import asyncio
from fastapi import HTTPException, status, WebSocket
from pony.orm import db_session
from typing import Dict, List

from database.dao.match_dao import update_finished_match
from database.models.models import Match 
from services.match import execute_match
from view_entities.match_view_entities import *
from view_entities.robot_view_entities import *


ERROR_CREATING_MATCH = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal error creating the match."
)

NOT_CREATOR = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Only the creator can start the match."
)

MATCH_ALREADY_STARTED = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The match has already started."
)

NOT_ENOUGH_PLAYERS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The minimum amount of players hasn't been reached."
)

INTERNAL_ERROR_UPDATING_MATCH_INFO = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal error when updating the match info."
)

INEXISTENT_ROBOT = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Robot selected is not in the user's library."
)

USER_ALREADY_JOINED = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The user has already joined."
)

INCORRECT_PASSWORD = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect password."
)

MAX_PLAYERS_REACHED = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Max players reached. Cannot join the match."
)

MATCH_ALREADY_STARTED = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The match has already started."
)

INEXISTENT_MATCH_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The match doesn't exist."
)

ERROR_DELETING_USER = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal error removing the user from the match."
)

USER_NOT_JOINED_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The user isn't in the match."
)

CREATOR_CANT_ABANDON_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The creator can't abandon the match."
)

MATCH_DOES_NOT_HAVE_PASSWORD = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The match does not have password."
)

# To handle websockets connections.
class LobbyManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        try:
            await websocket.close()
            self.active_connections.remove(websocket)
        except:
            pass

    # async def send_personal_message(self, message: str, websocket: WebSocket):
    #     await websocket.send_text(message)

    async def broadcast(self, message: Dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                await self.disconnect(connection)

    async def close_lobby(self):
        for connection in self.active_connections:
            await self.disconnect(connection)

lobbys: Dict[int, LobbyManager] = {}


# Transforms the matches selected from the database to the format that will be
# sent to the frontend.
@db_session
def match_db_to_view(matches: List[Match]): 
    matches_info = [MatchInfo.from_orm(m) for m in matches]
    all_robots_joined = []
    info_and_robots = []

    for m in matches:
       all_robots_joined.append(len(m.robots_joined))

    for i in range(0, len(matches_info)):
        info_and_robots.append(
            ShowMatch(
                match_id=matches_info[i].match_id,
                name=matches_info[i].name,
                creator_user=matches_info[i].creator_user,
                max_players=matches_info[i].max_players,
                robots_joined=all_robots_joined[i]
            )
        )

    return info_and_robots

@db_session
def match_validator_info(match_id: int):
    match_info = Match.get(match_id=match_id)
    if not match_info:
        return None
    else:
        return StartMatchValidator(
            min_players=match_info.min_players,
            started=match_info.started,
            robots_joined=len(match_info.robots_joined),
            creator_username=match_info.creator_user.username
        )


# This function is executed in another thread, it is called by the caller defined below
async def execute_match_task(match_id):
    winners = execute_match(match_id)

    if not update_finished_match(match_id):
        raise INTERNAL_ERROR_UPDATING_MATCH_INFO

    # SEND WINNERS TO SUSCRIBERS.
    await lobbys[match_id].broadcast({
        "action": "results",
        "data": {
            "winners" : winners
        }
    })

    # DELETE CONECTION MANAGER.
    await lobbys[match_id].close_lobby()
    lobbys.pop(match_id)


# This function executes the async function 'execute_match_task' in another thread.
# It is necessary because you can´t execute an async task in another thread directly.
def execute_match_task_caller(match_id):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(execute_match_task(match_id))
    loop.close()
