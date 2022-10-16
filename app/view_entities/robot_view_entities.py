from pydantic import BaseModel
from typing import Union

class BotCreate(BaseModel):
    owner_username: str
    name: str
    source_code: str
    avatar: Union[str, None] = None