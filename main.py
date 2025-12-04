from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database.database import engine, SessionLocal, Base
from typing import List
from routers import users, todoList, todoItems

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(todoList.router, prefix="/todo_lists", tags=["Todo Lists"])
app.include_router(todoItems.router, prefix="/todo_items", tags=["Todo Items"])