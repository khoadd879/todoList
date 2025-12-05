import shutil
import fastapi
from fastapi.security import HTTPBearer
from database.database import SessionLocal
from dependencies.auth import require_auth
from fastapi import UploadFile, File, Depends
from pathlib import Path
from sqlalchemy.orm import Session
from models import FileUpload

router = fastapi.APIRouter(dependencies=[fastapi.Depends(require_auth)])

security = HTTPBearer()

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True) 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/upload", response_model=None)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = UPLOAD_FOLDER / file.filename
    
    mimetype = file.content_type
    maintype = mimetype.split("/")[0]
    
    print(maintype)
    
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        record = FileUpload(
            path = str(file_path),
            type = maintype
        )
        
        db.add(record)
        db.commit()
        db.refresh(record)
        
        return {"message": "File uploaded successfully", 
                "data":{
            "id": record.id,
            "path": record.path,
            "type": record.type
        },
        "status": 200}
    except Exception as e:
        return {"error": str(e)}