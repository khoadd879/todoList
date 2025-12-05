from enum import Enum
from sqlalchemy import Column, String, Enum as SQLAlchemyEnum, ForeignKey
from database.database import Base
import uuid
from sqlalchemy.orm import relationship

class AccountStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DEACTIVE = "DEACTIVE"
    
class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashedPassword = Column(String, nullable=False)
    accessToken = Column(String, nullable=True)
    refreshToken = Column(String, nullable=True)
    status = Column(SQLAlchemyEnum(AccountStatus), default=AccountStatus.ACTIVE)
    
    user = relationship("Users", back_populates="account")
