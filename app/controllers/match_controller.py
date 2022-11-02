from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect, status, Header
from jose import jwt
from typing import Union, List, Dict

from database.dao.match_dao import *
from services.match import execute_match
from utils.match_utils import *
from utils.user_utils import *
from validators.match_validators import new_match_validator, start_match_validator
from validators.user_validators import validate_token, SECRET_KEY
from view_entities.match_view_entities import NewMatch


match_controller = APIRouter(prefix="/matches")


class LobbyManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        await websocket.close()
        self.active_connections.remove(websocket)

    # async def send_personal_message(self, message: str, websocket: WebSocket):
    #     await websocket.send_text(message)

    async def broadcast(self, message: Dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                self.disconnect(connection)
    
    async def close_lobby(self):
        for connection in self.active_connections:
            await self.disconnect(connection)

lobbys: Dict[str, LobbyManager] = {}


@match_controller.post("/new-match", status_code=status.HTTP_201_CREATED)
async def create_match(new_match: NewMatch, authorization: Union[str, None] = Header(None)):
    validate_token(authorization)

    token_data = jwt.decode(authorization, SECRET_KEY)
    
    creator_username = token_data['username']
    
    new_match_validator(creator_username, new_match)  
    
    created = create_new_match(creator_username, new_match)
    
    if not created:
        raise ERROR_CREATING_MATCH
    
    # Once added to the database, get the id assigned to the match and create
    # a websocket manager for the lobby
    match_id = get_match_by_name_and_user(new_match.name, creator_username).match_id
    lobbys[match_id] = LobbyManager()
    
    return True


@match_controller.get("/list-matches", status_code=status.HTTP_200_OK)
async def get_matches(authorization: Union[str, None] = Header(None)):   
   validate_token(authorization)

   matches_db = get_all_matches()
   
   matches_view = match_db_to_view(matches_db)
   
   return matches_view

@match_controller.post("/start-match/{match_id}", status_code=status.HTTP_200_OK)
async def start_match(match_id: int, authorization: Union[str, None] = Header(None)):
    validate_token(authorization)

    token_data = jwt.decode(authorization, SECRET_KEY)

    creator_username = token_data['username']

    start_match_validator(creator_username, match_id)

    ## SEND MESSAGE TO SUSCRIBERS, MATCH STARTED.

    await lobbys[match_id].broadcast({
        "action": "start",
        "data": ""
    })

    winners = execute_match(match_id)

    ## SEND WINNERS TO SUSCRIBERS.
    await lobbys[match_id].broadcast({
        "action": "results",
        "data": {
            "winners" : winners
        }
    })

    ## DELETE CONECTION MANAGER.
    await lobbys[match_id].close_lobby()
    lobbys.pop(match_id)

    ## UPDATE BD
    if not update_executed_match(match_id):
        raise INTERNAL_ERROR_UPDATING_MATCH_INFO

    return True

@match_controller.get("/join-lobby", status_code=status.HTTP_200_OK)
async def get_lobby(match_id: int, authorization: Union[str, None] = Header(None)):
    validate_token(authorization)
    token_data = jwt.decode(authorization, SECRET_KEY) 
    username = token_data['username']
    
    if get_match_by_id(match_id) is None:
        raise INEXISTENT_MATCH_EXCEPTION
    
    return get_lobby_info(match_id, username)
    
    
@match_controller.websocket("/ws/follow-lobby/{match_id}")
async def follow_lobby(
    websocket: WebSocket, 
    match_id: int,
    authorization: Union[str, None] = Query(None)
):
    validate_token(authorization)
    token_data = jwt.decode(authorization, SECRET_KEY) 
    username = token_data['username']
    
    if get_match_by_id(match_id) is None:
        raise INEXISTENT_MATCH_EXCEPTION
    
    await lobbys[match_id].connect(websocket)
    # print(f"{username} has now joined the lobby")
    while True:
        try:
            await websocket.receive_text()
        except WebSocketDisconnect:
            # print(f"{username} web socket connection closed")
            return
