from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List
from database.database import SessionLocal 
import crud, schemas
from dependencies.auth import require_auth

router = APIRouter(dependencies=[Depends(require_auth)])

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=None) 
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    users = crud.create_user(db=db, user=user)
    return {
        "message": "User created successfully",
        "data": users,
        "status_code": 200
    }

@router.get("/") 
async def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    if not users:
        return {
            "message": "No users found",
            "data": [],
            "status_code": 404
        }
    return {
        "message": "Users are retrieved successfully",
        "data": users,
        "status_code": 200
    }

@router.put("/users/{user_id}")
async def update_user(user_id: str, user: schemas.UserCreate, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db=db, user_id=user_id, user=user)
    if(not updated_user):
        return {
            "message": "User not found",
            "data": None,
            "status_code": 404
        }
    return {"message": "User is updated successfully","data": updated_user,"status code": 200}

@router.delete("/users/{user_id}")
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    result = crud.delete_user(db=db, user_id=user_id)
    if(not result):
        return {
            "message": "User not found",
            "data": None,
            "status_code": 404
        }
    return {"message": "User is deleted successfully","status code": 200}