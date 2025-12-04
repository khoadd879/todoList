from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from models.users import Gender
# Có thể import TodoListResponse nếu muốn hiện list công việc của user (cẩn thận vòng lặp)
# from .todoLists import TodoListResponse 

class UserBase(BaseModel):
    name: str
    gender: Gender
    dob: Optional[datetime] = None

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: str
    createdAt: datetime
    updatedAt: datetime
    
   
    class Config:
        from_attributes = True