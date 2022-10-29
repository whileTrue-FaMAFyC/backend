from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect, status, Header
from jose import jwt
from typing import Union, List, Dict

from database.dao.match_dao import *
from utils.match_utils import *
from utils.user_utils import *
from validators.match_validators import new_match_validator
from validators.user_validators import validate_token, SECRET_KEY
from view_entities.match_view_entities import NewMatch


match_controller = APIRouter(prefix="/matches")


class LobbyManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    # async def send_personal_message(self, message: str, websocket: WebSocket):
    #     await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

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
    match_id = get_match_by_name_and_user(new_match.name, creator_username)
    lobbys[match_id] = LobbyManager()
    
    return True


@match_controller.get("/list-matches", status_code=status.HTTP_200_OK)
async def get_matches(authorization: Union[str, None] = Header(None)):   
   validate_token(authorization)

   matches_db = get_all_matches()
   
   matches_view = match_db_to_view(matches_db)
   
   return matches_view


@match_controller.get("/join-lobby", status_code=status.HTTP_200_OK)
async def get_lobby(match_id: int, authorization: Union[str, None] = Header(None)):
    validate_token(authorization)
    
    return get_lobby_info(match_id)
    
    
async def get_token(
    websocket: WebSocket,
    token: Union[str, None] = Query(default=None)
):
    if token is None:
        raise INVALID_TOKEN_EXCEPTION
    return token

    
@match_controller.websocket("/ws/follow-lobby/{match_id}")
async def follow_lobby(
    websocket: WebSocket, 
    match_id: int,
    token: str = Depends(get_token)
):
    token_data = jwt.decode(token, SECRET_KEY) 
    username = token_data['username']
    
    await lobbys[match_id].connect(websocket)
    print(f"{username} has now joined the lobby")
    
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
    except WebSocketDisconnect:
        lobbys[match_id].disconnect(websocket)
        print(f"{username} left the lobby")
