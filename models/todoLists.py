import uuid
from enum import Enum
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime

class Status(str, Enum):
    UNFINISHED = "Unfinished"
    FINISH = "Finish"
    
class TodoList(Base):
    __tablename__ = "todo_list"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True)
    status = Column(SQLAlchemyEnum(Status), default=Status.UNFINISHED)
    user_id = Column(String, ForeignKey("users.id"))
    createdAt = Column(DateTime, default=datetime.now)
    updatedAt = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    items = relationship("TodoItem", back_populates="todo_list")
    
    owner = relationship("Users", back_populates="todo_lists")