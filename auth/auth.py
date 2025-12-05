from datetime import datetime, timedelta, date
import os
from typing import Optional
import jwt
from sqlalchemy.orm import Session
from fastapi import Depends
from typing_extensions import Annotated
from fastapi import APIRouter
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from database.database import SessionLocal
from routers.todoItems import get_db
from models import Account, Users, Gender
import hashlib
from passlib.handlers.bcrypt import bcrypt
from jwt import ExpiredSignatureError, InvalidTokenError

load_dotenv()

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY", "mat_khau_mac_dinh_cho_dev")
REFRESH_SECRET_KEY= os.getenv("REFRESH_SECRET_KEY", "12311212414at_khau_mac_dinh_cho_dev")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES= 300

print("PWD:", os.getcwd())
print("SECRET_KEY used:", SECRET_KEY)
print("REFRESH_SECRET_KEY used:", REFRESH_SECRET_KEY)


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer= OAuth2PasswordBearer(tokenUrl="auth/token")

class CreateAccount(BaseModel):
    username: str
    password: str
    confirmPassword: str

class LoginData(BaseModel):
    username: str
    password: str
    
class TokenData(BaseModel):
    token: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

#Tao access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#Tao refresh token
def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode["exp"] = expire
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

#Dang ky
@router.post("/register", response_model=None)
async def register_account(account: CreateAccount, db: db_dependency):
    existing_account = db.query(Account).filter(Account.username == account.username).first()
    if existing_account:
        return {
            "message": "Username already exists",
            "data": None,
            "status_code": 400
        }

    if account.password != account.confirmPassword:
        return {
            "message": "Passwords do not match",
            "data": None,
            "status_code": 400
        }
    
    sha256_pass = hashlib.sha256(account.password.encode()).hexdigest()

    hashed_password = bcrypt_context.hash(sha256_pass)
    
    new_user = Users(
        name=None,
        gender=Gender.MALE,
        dob=None
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    new_account = Account(
        username=account.username,
        hashedPassword=hashed_password,
        user_id=new_user.id
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    
    return {
        "message": "Account and User profile created successfully", 
        "account_id": new_account.id,
        "user_id": new_user.id,
        "status_code": 200
    }
    
#Dang Nhap
@router.post("/login", response_model=None)
async def login(
    form_data: Annotated[LoginData, Depends()],
    db: db_dependency
):
    username = form_data.username
    password = form_data.password
    
    account = db.query(Account).filter(Account.username == username).first()
    if not account:
        return {
            "message": "Invalid username or password",
            "data": None,
            "status_code": 401
        }

    if account.accessToken or account.refreshToken:
        account.accessToken = None
        account.refreshToken = None
        db.commit()
        db.refresh(account)

    # verify password
    sha256_pass = hashlib.sha256(password.encode()).hexdigest()
    if not bcrypt_context.verify(sha256_pass, account.hashedPassword):
        return {
            "message": "Invalid username or password",
            "data": None,
            "status_code": 401
        }

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
        "sub": account.username,    
        "user_id": account.user_id  
    }, expires_delta=access_token_expires
    )
    
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_refresh_token(
        data={
        "sub": account.username,    
        "user_id": account.user_id  
    }, expires_delta=refresh_token_expires
    )
    
    if access_token and refresh_token:
        account.accessToken = access_token
        account.refreshToken = refresh_token
        db.commit()
        db.refresh(account)


    return {
        "message": "Login successful",
        "data":{
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        },
        "status_code": 200
    }

#Kiem tra xem access con hoat dong hay khong
@router.post("/introspect_access")
async def introspect_access(data: TokenData):
    try:
        payload = jwt.decode(data.token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"active": True, "payload": payload}
    except ExpiredSignatureError:
        return {"active": False, "reason": "expired"}
    except InvalidTokenError:
        return {"active": False, "reason": "invalid"}


@router.post("/introspect_refresh")
async def introspect_refresh(data: TokenData):
    try:
        payload = jwt.decode(data.token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        return {"active": True, "payload": payload}
    except ExpiredSignatureError:
        return {"active": False, "reason": "expired"}
    except InvalidTokenError:
        return {"active": False, "reason": "invalid"}
    
#Refresh token
@router.post("/refresh_token")
async def refresh_token(data: TokenData, db: db_dependency):

    check = await introspect_refresh(TokenData(token=data.token))

    if not check["active"]:
        return {
            "message": "Refresh token invalid or expired",
            "status_code": 401
        }

    sub = check["payload"]
    
    username = sub.get("sub")
    user_id = sub.get("user_id")

    new_access_token = create_access_token(
        data={
        "sub": username,    
        "user_id": user_id  
    },
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "message": "New access token created",
        "access_token": new_access_token,
        "status_code": 200
    }
