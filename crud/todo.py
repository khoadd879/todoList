from sqlalchemy.orm import Session
from models.todoItems import TodoItem
from models.todoLists import TodoList
from schemas.todoLists import TodoListCreate
from schemas.todoItems import TodoItemCreate

# Hàm lấy danh sách todo list
def get_todoLists(db: Session):
    return db.query(TodoList).all()

# Hàm tạo todo list mới
def create_todoList(db: Session, todoList: TodoListCreate):
    db_todoList = TodoList(
        name=todoList.name,
        status=todoList.status,
        user_id=todoList.user_id,
    )
    db.add(db_todoList)
    db.commit()
    db.refresh(db_todoList)
    return db_todoList

# Hàm cập nhật todo list
def update_todoList(db: Session, todoList_id: str, todoList: TodoListCreate):
    db_todoList = db.query(TodoList).filter(TodoList.id == todoList_id).first()
    if db_todoList:
        db_todoList.name = todoList.name
        db_todoList.status = todoList.status
        db.commit()
        db.refresh(db_todoList)
        return db_todoList
    return None

# Hàm quản lý todo items liên quan đến todo list
def get_todoItems_by_todoList(db: Session, todoList_id: str):
    return db.query(TodoList).filter(TodoList.id == todoList_id).first()

#Ham xoa todo list lan items thuoc todo list do
def delete_todoList_with_items(db: Session, todoList_id: str):
    todo_list = get_todoItems_by_todoList(db, todoList_id)
    if todo_list:
        for item in todo_list.items:
            db.delete(item)
        db.delete(todo_list)
        db.commit()
        return True
    return None

#Ham xoa item
def delete_todoItem(db: Session, item_id: str):
    todo_item = db.query(TodoItem).filter(TodoItem.id == item_id).first()
    if todo_item:
        db.delete(todo_item)
        db.commit()
        return True
    return None

#Ham tao todo item thuoc todo list
def create_todoItems_for_todoList(db: Session, todoList_id: str, items_data: list[TodoItemCreate]):
    todo_list = get_todoItems_by_todoList(db, todoList_id)
    if not todo_list:
        return None

    created_items = []
    for item_schema in items_data:
        new_item = TodoItem(
            name=item_schema.name,
            des=item_schema.des,
            due_at=item_schema.due_at,
            status=item_schema.status,
            todo_group_id=todoList_id
        )
        db.add(new_item)
        created_items.append(new_item)
    
    db.commit()
    return True

#Ham lay todo list kem theo todo items
def get_todoList_with_items(db: Session, todoList_id: str):
    todo_list = db.query(TodoList).filter(TodoList.id == todoList_id).first()

    if not todo_list:
        return None

    items = todo_list.items   

    return todo_list

#Ham cap nhat todo items thuoc todo list
def update_todoItems(db: Session, todoList_id: str, todoItem_id: str, items_data: TodoItemCreate):
    todo_list = get_todoItems_by_todoList(db, todoList_id)
    if not todo_list:
        return None
    todo_item = db.query(TodoItem).filter(TodoItem.id == todoItem_id).first()
    if not todo_item:
        return None
    if todo_list and todo_item:
        todo_item.name = items_data.name
        todo_item.des = items_data.des
        todo_item.due_at = items_data.due_at
        todo_item.status = items_data.status
        todo_item.todo_group_id = items_data.todo_group_id
        db.commit()
        return True
    return None
