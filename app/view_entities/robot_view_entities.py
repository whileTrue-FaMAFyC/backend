from pydantic import BaseModel
from typing import Union

class BotCreate(BaseModel):
    name: str
    source_code: str
    bot_filename: str
    avatar: Union[str, None] = None