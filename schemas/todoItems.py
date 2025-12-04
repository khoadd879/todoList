from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.todoItems import Status as ItemStatus

# Class cơ bản chứa các trường chung
class TodoItemBase(BaseModel):
    name: str
    des: Optional[str] = None
    due_at: Optional[datetime] = None
    status: ItemStatus = ItemStatus.TODO

# Class dùng để TẠO (Create) - Client gửi lên
class TodoItemCreate(TodoItemBase):
    todo_group_id: str 

# Class dùng để TRẢ VỀ (Response) - Server trả về
class TodoItemResponse(TodoItemBase):
    id: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True