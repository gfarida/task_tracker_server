from typing import Optional
from pydantic import BaseModel, ConfigDict


class STaskAdd(BaseModel):
    name: str
    description: Optional[str] = None

class STask(STaskAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

class STaskId(BaseModel):
    ok: bool = True
    task_id: int

class SStatus(BaseModel):
    ok: bool = True


class SUserLogin(BaseModel):
    username: str
    password: str

class SUser(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)