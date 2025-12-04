
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Enum as SQLAlchemyEnum   
from enum import Enum
from database.database import Base
import uuid

class Status(str, Enum):
    TODO = "Todo"
    IN_PROCESS = "In-Process"
    FINISH = "Finish"

class TodoItem(Base):
    __tablename__ = "todo_items"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    todo_group_id = Column(String, ForeignKey("todo_list.id"))
    name = Column(String, index=True)
    des = Column(String, index=True)
    due_at = Column(DateTime, index=True)
    status = Column(
    SQLAlchemyEnum(Status, values_callable=lambda x: [e.value for e in x], native_enum=False),
    default=Status.TODO
    )

    createdAt = Column(DateTime, default=datetime.now)
    updatedAt = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    todo_list = relationship("TodoList", back_populates="items")