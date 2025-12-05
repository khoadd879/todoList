from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database.database import SessionLocal 
import crud, schemas
from dependencies.auth import require_auth

router = APIRouter(dependencies=[Depends(require_auth)])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/")
async def create_todoList(todoList: schemas.TodoListCreate, db: Session = Depends(get_db)):
    todo_list = crud.create_todoList(db=db, todoList=todoList)
    return {
        "message": "Todo list created successfully",
        "data": todo_list,
        "status_code": 200
    }

@router.get("/")
async def read_todoLists(db: Session = Depends(get_db)):
    todo_lists = crud.get_todoLists(db)
    if not todo_lists:
        return {
            "message": "No todo lists found",
            "data": [],
            "status_code": 404
        }
    return {
        "message": "Todo lists are retrieved successfully",
        "data": todo_lists,
        "status_code": 200
    }
    
@router.put("/todo_lists/{todoList_id}")
def update_todoList(todoList_id: str, todoList: schemas.TodoListCreate, db: Session = Depends(get_db)):
    updated_todo_list = crud.update_todoList(db=db, todoList_id=todoList_id, todoList=todoList)
    if not updated_todo_list:
        return {
            "message": "Todo list not found",
            "data": None,
            "status_code": 404
        }
    return {
        "message": "Todo list is updated successfully",
        "data": updated_todo_list,
        "status_code": 200
    }
    
@router.delete("/todo_lists/{todoList_id}/items")
async def delete_todoList_with_items(todoList_id: str, db: Session = Depends(get_db)):
    result = crud.delete_todoList_with_items(db=db, todoList_id=todoList_id)
    if not result:
        return {
            "message": "Todo list not found",
            "data": None,
            "status_code": 404
        }
    return {
        "message": "Todo items deleted successfully",
        "status_code": 200
    }