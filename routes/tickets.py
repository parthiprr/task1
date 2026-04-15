from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models.ticket import Ticket
from schemas.ticket import TicketCreate
from fastapi import BackgroundTasks
from tasks import process_ticket
from schemas.ticket import TicketUpdate
from fastapi import HTTPException
from utils.deps import get_current_user
from models.user import User
from utils.deps import require_admin


router = APIRouter()

def process_ticket(ticket_id: int):
    print(f"Background Task Running: Ticket {ticket_id} processed")

@router.post("/")
async def create_ticket(
    ticket: TicketCreate,
    background_tasks: BackgroundTasks, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        user_id=current_user.id
    )
    db.add(new_ticket)
    await db.commit()
    await db.refresh(new_ticket)
    background_tasks.add_task(process_ticket, new_ticket.id)
    
    return new_ticket
    
    
@router.get("/")
async def get_tickets(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Ticket).where(Ticket.user_id == current_user.id)
    )
    return result.scalars().all()

from fastapi import HTTPException

@router.delete("/{ticket_id}")
async def delete_ticket(
    ticket_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)):
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    await db.delete(ticket)
    await db.commit()

    return {"message": "Ticket deleted successfully"}


@router.put("/{ticket_id}")
async def update_ticket(
    ticket_id: int,
    ticket_update: TicketUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
    ):
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if ticket_update.status is not None:
        ticket.status = ticket_update.status

    await db.commit()
    await db.refresh(ticket)

    return ticket
