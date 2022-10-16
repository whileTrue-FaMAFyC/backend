from pydantic import BaseModel
from typing import Union

class BotCreate(BaseModel):
    access_token: str
    name: str
    source_code: str
    avatar: Union[str, None] = None