from pydantic import BaseModel

class NewRobotTest(BaseModel):
    name: str
    email: str
    avatar: str = ""
    source_code: str
