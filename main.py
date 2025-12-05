from fastapi import FastAPI
from fastapi.security import HTTPBearer
from database.database import engine, Base
from routers import users, todoList, todoItems
from auth import auth

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(todoList.router, prefix="/todo_lists", tags=["Todo Lists"])
app.include_router(todoItems.router, prefix="/todo_items", tags=["Todo Items"])