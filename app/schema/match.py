from pydantic import BaseModel

class Username(BaseModel):
   username : str
 
   class Config:
       orm_mode = True
 
class ShowMatchSchema(BaseModel):
   name: str
   creator_user: Username
   min_players: int
   max_players: int
   num_games: int
   num_rounds: int
 
   class Config:
       orm_mode = True