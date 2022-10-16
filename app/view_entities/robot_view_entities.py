from pydantic import BaseModel
from typing import Union

class NewRobotTest(BaseModel):
    name: str
    email: str
    avatar: Union[str, None] = None
    source_code: str
