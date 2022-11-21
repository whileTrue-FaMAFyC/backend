from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect, status, Header, Depends
from jose import jwt
from threading import Thread
from typing import Union

from database.dao.match_dao import *
from database.dao.robot_dao import *
from database.dao.user_dao import *
from utils.match_utils import *
from utils.user_utils import *
from validators.match_validators import *
from validators.user_validators import validate_token, SECRET_KEY
from view_entities.match_view_entities import NewMatch, JoinMatch, MatchesFilters



match_controller = APIRouter(prefix="/matches")


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
async def get_matches(
    filters: MatchesFilters = Depends(),
    authorization: Union[str, None] = Header(None)
):
    validate_token(authorization)
    token_data = jwt.decode(authorization, SECRET_KEY)
    user = token_data['username']
    
    matches_db = get_matches_with_filter(
        filters.is_owner,
        filters.is_joined,
        filters.started, user
    )

    return match_db_to_view(matches_db)



@match_controller.put("/start-match/{match_id}", status_code=status.HTTP_200_OK)
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

    ## UPDATE BD
    if not update_executed_match(match_id):
        raise INTERNAL_ERROR_UPDATING_MATCH_INFO

    # Execute the match in another thread and returns the HTTP response with 200 OK.
    match_execution_thread = Thread(target=execute_match_task_caller, args=[match_id])
    match_execution_thread.start()

    return True


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
       await websocket.close()
       return
    
    if match.finished:
       await websocket.close()
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


@match_controller.delete("/leave-match/{match_id}", status_code=status.HTTP_200_OK)
async def leave_match(match_id: int, authorization: Union[str, None] = Header(None)):
    validate_token(authorization)
    token_data = jwt.decode(authorization, SECRET_KEY)
    leaving_user = token_data['username']

    leave_match_validator(match_id, leaving_user)

    leaving_robot = get_robot_in_match_by_owner(match_id, leaving_user)
    
    if not update_leaving_user(match_id, leaving_user):
        raise ERROR_DELETING_USER
    
    # SEND MESSAGE TO SUSCRIBERS
    message_to_broadcast = {
        "action": "leave",
        "data": {
            "username": leaving_user,
            "user_avatar": get_user_avatar(leaving_user),
            "robot_name": leaving_robot.name,
            "robot_avatar": get_robot_avatar_by_name_and_owner(leaving_user, leaving_robot.name)
        }
    }
    
    await lobbys[match_id].broadcast(message_to_broadcast)
    
    return True
