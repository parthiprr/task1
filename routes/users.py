from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserCreate

router = APIRouter()

@router.post("/")
async def create_user(user:UserCreate,db:Session=Depends(get_db)):
    new_user=User(name=user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/")
async def get_users(db:Session=Depends(get_db)):
    return db.query(User).all()