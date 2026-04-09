from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models.ticket import Ticket
from schemas.ticket import TicketCreate

router = APIRouter()

@router.post("/")
async def create_ticket(ticket: TicketCreate, db: AsyncSession = Depends(get_db)):
    new_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        user_id=ticket.user_id
    )
    db.add(new_ticket)
    await db.commit()
    await db.refresh(new_ticket)
    
    return new_ticket
    
    
@router.get("/")
async def get_tickets(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Ticket))
    return result.scalars().all()