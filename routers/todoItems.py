from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database.database import SessionLocal 
import crud, schemas
import schemas
from schemas.todoItems import TodoItemCreate
from dependencies.auth import require_auth

router = APIRouter(dependencies=[Depends(require_auth)])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/todo_lists/{todoList_id}/items")
async def create_todoItems_for_todoList(todoList_id: str, items_data: List[schemas.TodoItemCreate], db: Session = Depends(get_db)):
    created_items = crud.create_todoItems_for_todoList(db=db, todoList_id=todoList_id, items_data=items_data)
    if not created_items:
        return {
            "message": "Todo list not found",
            "data": None,
            "status_code": 404
        }
    return {
        "message": "Todo items created successfully",
        "data": created_items,
        "status_code": 200
    }
    
@router.get("/todo_lists/{todoList_id}/items")
async def read_todoList_with_items(todoList_id: str, db: Session = Depends(get_db)):
    todo_list = crud.get_todoList_with_items(db=db, todoList_id=todoList_id)
    if not todo_list:
        return {
            "message": "Todo list not found",
            "data": None,
            "status_code": 404
        }
    return {
        "message": "Todo list with items retrieved successfully",
        "data": todo_list,
        "status_code": 200
    }
    
@router.put("/{todoList_id}/{todoItem_id}")
async def update_todoItems(todoList_id: str, todoItem_id: str, items_data: TodoItemCreate, db: Session = Depends(get_db)):   
    updated_items = crud.update_todoItems(db=db, todoItem_id=todoItem_id, todoList_id=todoList_id, items_data=items_data)
    if not updated_items:
        return {
            "message": "Todo list not found",
            "data": None,
            "status_code": 404
        }
    return {
        "message": "Todo items updated successfully",
        "data": updated_items,
        "status_code": 200
    }

@router.delete("/items/{item_id}")    
async def delete_todoItem(item_id: str, db: Session = Depends(get_db)):
    result = crud.delete_todoItem(db=db, item_id=item_id)
    if not result:
        return {
            "message": "Todo item not found",
            "data": None,
            "status_code": 404
        }
    return {
        "message": "Todo item deleted successfully",
        "status_code": 200
    }