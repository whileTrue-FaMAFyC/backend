from fastapi import APIRouter, status, Header
from jose import jwt
from typing import Union

from database.dao.robot_dao import get_bot_by_owner_and_name
from services.simulation import execute_simulation
from validators.user_validators import validate_token, SECRET_KEY
from validators.simulation_validators import simulation_validator
from view_entities.robot_view_entities import RobotInSimulation
from view_entities.simulation_view_entities import Simulation


simulation_controller = APIRouter()

@simulation_controller.post("/new-simulation", status_code=status.HTTP_201_CREATED)
async def create_simulation(simulation_info: Simulation, 
                            authorization: Union[str, None] = Header(None)):
    validate_token(authorization)

    token_data = jwt.decode(authorization, SECRET_KEY)
    
    creator_username = token_data['username']
    
    simulation_validator(creator_username, simulation_info)  

    frames, robots, winners = execute_simulation(creator_username, simulation_info)
    
    return {
        "names": robots,
        "simulation": frames,
        "winners": winners
    }