from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models.user import User
from schemas.user import UserCreate

router = APIRouter()

@router.post("/")
async def create_user(user:UserCreate,db:AsyncSession=Depends(get_db)):
    new_user=User(name=user.name)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.get("/")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()