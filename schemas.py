from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str
    is_completed: bool

class TaskOut(BaseModel):
    id: int
    title: str
    is_completed: bool

    class Config:
        orm_mode = True
