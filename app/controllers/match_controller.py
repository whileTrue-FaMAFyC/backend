from ssl import match_hostname
from fastapi import APIRouter, WebSocket, status, Header
from jose import jwt
from typing import Union, List, Dict

from database.dao import match_dao
from utils.match_utils import ERROR_CREATING_MATCH, match_db_to_view
from utils.user_utils import *
from validators.match_validators import new_match_validator
from validators.user_validators import validate_token, SECRET_KEY
from view_entities.match_view_entities import NewMatch


match_controller = APIRouter(prefix="/matches")


# Class to handle the connection of different clients
class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    # The client (`websocket`) starts to accept message from the browser and is 
    # added to a list with all the clients.
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    # Broadcasts `data` to any other client in the room
    async def broadcast(self, data: str):
        for connection in self.connections:
            await connection.send_text(data)

lobbys: Dict[str, ConnectionManager] = {}


@match_controller.post("/new-match", status_code=status.HTTP_201_CREATED)
async def create_match(new_match: NewMatch, authorization: Union[str, None] = Header(None)):
    validate_token(authorization)

    token_data = jwt.decode(authorization, SECRET_KEY)
    
    creator_username = token_data['username']
    
    new_match_validator(creator_username, new_match)  
    
    created = match_dao.create_new_match(creator_username, new_match)
    
    if not created:
        raise ERROR_CREATING_MATCH
    return True


@match_controller.get("/list-matches", status_code=status.HTTP_200_OK)
async def get_matches(authorization: Union[str, None] = Header(None)):   
   validate_token(authorization)

   matches_db = match_dao.get_all_matches()
   
   matches_view = match_db_to_view(matches_db)
   
   return matches_view


@match_controller.websocket("ws/join-lobby/{creator_username}/{match_name}")
async def join_lobby(
    websocket: WebSocket,
    creator_username: str,
    match_name: str
):
    token = websocket.headers['sec-websocket-protocol']
    print(token)
    
    # validate_token(token)

    lobbys[creator_username + "_" + match_name].connect(websocket)
    print(lobbys[creator_username + "_" + match_name].connections)
    pass