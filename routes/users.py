from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models.user import User

from schemas.user import UserCreate
from utils.auth import hash_password,verify_password,create_access_token
from schemas.user import UserLogin
from fastapi.security import OAuth2PasswordRequestForm

from app.messaging.producer import publish_message


router = APIRouter()


@router.post("/register")
async def create_user(user:UserCreate,db:AsyncSession=Depends(get_db)):
    new_user=User(
        name=user.name,
        password=hash_password(user.password),
        role=user.role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    publish_message({
    "type": "user_registered",
    "user": user.name
})
    return new_user


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.name == form_data.username)
    )
    db_user = result.scalar_one_or_none()

    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)})

    return {"access_token": token, "token_type": "bearer"}

@router.get("/")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()