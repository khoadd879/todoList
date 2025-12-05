import uuid
from database.database import Base
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Enum as SQLAlchemyEnum
from datetime import datetime

class FileUpload(Base):
    __tablename__ = "files"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    path = Column(String)
    type = Column(String)
    createdAt= Column(DateTime, default=datetime.now)
    