from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect, status, Header
from jose import jwt
from typing import Union, List, Dict

from database.dao.match_dao import *
from database.dao.robot_dao import *
from database.dao.user_dao import *
from utils.match_utils import *
from utils.user_utils import *
from validators.match_validators import new_match_validator, join_match_validator
from validators.user_validators import validate_token, SECRET_KEY
from view_entities.match_view_entities import NewMatch, JoinMatch


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

    async def broadcast(self, message: Dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                self.disconnect(connection)


lobbys: Dict[int, LobbyManager] = {}


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


@match_controller.post("/join-match/{match_id}", status_code=status.HTTP_200_OK)
async def join_match(match_id: int, match: JoinMatch, authorization: Union[str, None] = Header(None)):
    validate_token(authorization)

    token_data = jwt.decode(authorization, SECRET_KEY)
    
    joining_user = token_data['username']

    join_match_validator(joining_user, match, match_id)

    if not update_joining_user_match(joining_user, match.joining_robot, match_id):
        raise INTERNAL_ERROR_UPDATING_MATCH_INFO

    ## SEND MESSAGE TO SUSCRIBERS. CANNOT SEND PYDANTIC MODELS, WE USE A DICT.
    message_to_broadcast = {
        "action": "join",
        "data": {
            "username": joining_user,
            "user_avatar": get_user_avatar(joining_user),
            "robot_name": match.joining_robot,
            "robot_avatar": get_robot_avatar_by_name_and_owner(joining_user, match.joining_robot)
        }
    }

    await lobbys[match_id].broadcast(message_to_broadcast)

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
    
    match = get_match_by_id(match_id)
    if match is None:
       websocket.close()
       return
    
    if match.started:
       websocket.close()
       return
 
    if not match_id in lobbys:
        lobbys[match_id] = LobbyManager()

    await lobbys[match_id].connect(websocket)
    # print(f"{username} has now joined the lobby")
    while True:
        try:
            await websocket.receive_text()
        except WebSocketDisconnect:
            # print(f"{username} web socket connection closed")
            return
