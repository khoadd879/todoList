from sqlalchemy.orm import Session
from models.users import Users
from schemas.users import UserCreate
import uuid

# Hàm lấy danh sách user
def get_users(db: Session):
    return db.query(Users).all()

# Hàm tạo user mới
def create_user(db: Session, user: UserCreate):
    db_user = Users(
        name=user.name,
        gender=user.gender,
        dob=user.dob
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: str, user: UserCreate):
    db_user = db.query(Users).filter(Users.id == user_id).first()
    if db_user:
        db_user.name = user.name
        db_user.gender = user.gender
        db_user.dob = user.dob
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def delete_user(db: Session, user_id: str):
    db_user = db.query(Users).filter(Users.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return None