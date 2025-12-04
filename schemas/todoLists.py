from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from models.todoLists import Status as ListStatus
from .todoItems import TodoItemResponse

class TodoListBase(BaseModel):
    name: str
    status: ListStatus = ListStatus.UNFINISHED
    user_id: str

class TodoListCreate(TodoListBase):
    pass

class TodoListResponse(TodoListBase):
    id: str
    createdAt: datetime
    updatedAt: datetime
    
    items: List[TodoItemResponse] = [] 

    class Config:
        from_attributes = True