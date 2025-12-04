from datetime import datetime
import uuid
from enum import Enum
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from database.database import Base

class Gender(str, Enum):
    MALE = "M"
    FEMALE = "F"

class Users(Base):
    __tablename__ = "users"
    
    id =  Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name =  Column(String, index=True)
    gender = Column(SQLAlchemyEnum(Gender), nullable=False)
    dob = Column(DateTime)
    createdAt = Column(DateTime, default=datetime.now)
    updatedAt = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    todo_lists = relationship("TodoList", back_populates="owner")