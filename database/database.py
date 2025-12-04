from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL kết nối (từ Docker)
DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/todo_db"

# 1. Tạo Engine
engine = create_engine(DATABASE_URL)

# 2. Tạo SessionLocal (để sau này dùng trong mỗi request API)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Tạo Base (Class cha cho các model)
Base = declarative_base()