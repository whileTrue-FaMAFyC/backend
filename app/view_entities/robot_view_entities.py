from fastapi import UploadFile
from pydantic import BaseModel
from typing import Union

class NewRobotTest(BaseModel):
    name: str
    email: str
    avatar: Union[UploadFile, None] = None
    source_code: str
