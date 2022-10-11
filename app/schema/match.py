from pydantic import BaseModel, validator
from typing import List

class Username(BaseModel):
    username: str
    
    class Config:
        orm_mode = True
 
 
class Robot(BaseModel):
    owner : Username
    
    class Config:
        orm_mode = True
 
class ShowMatchSchema(BaseModel):
    name: str
    creator_user: Username
    min_players: int
    max_players: int
    num_games: int
    num_rounds: int
    robots_joined: List[Robot]
    
    @validator("robots_joined", pre=True, allow_reuse=True)
    def pony_set_to_list(cls, v):
        return list(v)
    class Config:
        orm_mode = True
