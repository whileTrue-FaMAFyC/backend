from pydantic import BaseModel
from typing import List

class Simulation(BaseModel):
    num_rounds: int
    robots: List[str]

    class Config:
        orm_mode = True
